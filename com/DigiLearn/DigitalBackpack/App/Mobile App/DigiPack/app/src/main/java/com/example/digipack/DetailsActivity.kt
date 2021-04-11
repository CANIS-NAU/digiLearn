package com.example.digipack

import DigiJson.DigiDrive
import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_details.*
import kotlinx.coroutines.*
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import org.json.JSONObject
import util.CacheUtility
import util.ServerInteraction

class DetailsActivity : AppCompatActivity() {
    private val scope = MainScope()
    //call the network detector tool
    private val networkMonitor = networkDetectorTool(this)

    private lateinit var flintent : Intent
    private lateinit var gclassIntent : Intent
    private lateinit var gsearchIntent : Intent
    private var layoutselection : Boolean = false

    override fun onCreate( savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_details)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>DigiPack</font>");

        var guser = intent.getSerializableExtra("guser") as GUser
        google_first_name_textview.text = guser.firstName
        layoutSelection()

        //call the network detector
        //runOnUiThread{
            networkMonitor.result = { isAvailable, type ->
                when( isAvailable ){
                    true -> { clouds.setImageResource(R.drawable.sun_connection)
                                connectToServer(guser)
                    }
                    else -> { clouds.setImageResource(R.drawable.networkclouds)
                                buildActivitiesFromCache(guser)
                    }
                }
            }
        //}
    }

    private fun layoutSelection(){
        normlayout.setOnClickListener {
            layoutselection = false
            Toast.makeText(this, "Normal UI Selected", Toast.LENGTH_SHORT).show()
        }
        kidslayout.setOnClickListener {
            layoutselection = true
            Toast.makeText(this, "Kids UI Selected", Toast.LENGTH_SHORT).show()
        }
    }

    private fun connectToServer(guser: GUser)= scope.launch{
        val DA = this@DetailsActivity
        val fso = intent.getBooleanExtra("firstSignIn", true)
        val server = ServerInteraction(DA, scope)
        if(DA::flintent.isInitialized){
            Log.i(getString(R.string.app_name), "Details_act: file list intent already initialized")
        }
        else{
            flintent = Intent(DA, FileListViewActivity::class.java)
            val fileres = getFileList(server, guser)
        }
        Log.i(getString(R.string.app_name), "connect to server finished")
    }

    private suspend fun getFileList(server: ServerInteraction, guser: GUser) {

        val filelist = withContext(Dispatchers.IO){
            server.getFileList(guser)
        }
        withContext(Dispatchers.Main){
            flintent.putExtra("guser", guser)
            flintent.putExtra("filelist", filelist)
            Log.i(getString(R.string.app_name), "getFileList: extras added")
        }
    }

    // When menu bar is clicked
    override fun onCreateOptionsMenu(menu: Menu): Boolean {

        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu, menu)
        return true
    }

    // Function to do when items on the menu option are clicked
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        val id = item.itemId

        //case google drive button
        if (id == R.id.googleDriveBtn) {
            when{
                // Go to the Google Drive page if initialized
                this::flintent.isInitialized -> {
                    flintent.putExtra("layoutselection", layoutselection)
                    startActivity(flintent)
                }
                //else, google drive intent not initialized; block activity and report unavailable
                else ->{
                    Toast.makeText(this, "Google Drive not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
            return true
        }
        /** COMMENTING OUT UNTIL THE FILE LIST WORKS
        //case google class button
        if (id == R.id.googleClassBtn) {
            when{
                // Go to GClass page if initialized
                this::gclassIntent.isInitialized -> {
                    gclassIntent.putExtra("layoutselection", layoutselection)
                    startActivity(gclassIntent)
                }
                //else, google class intent not initialized; block activity and report unavailable
                else ->{
                    Toast.makeText(this, "Google Classroom not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
            return true
        }

        //case google search button
        if (id == R.id.googleSearchBtn) {
            when{
                // Go to GSearch Page if initialized
                this::gsearchIntent.isInitialized -> {
                    gsearchIntent.putExtra("layoutselection", layoutselection)
                    startActivity(gsearchIntent)
                }
                //else, google search intent not initialized; block activity and report unavailable
                else ->{
                    Toast.makeText(this, "Google Search not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
            return true
        }
        **/
        return super.onOptionsItemSelected(item)
    }
    /**
     * When the network is unavailable, attempts to retrieve GClass, GDrive data from cache.
     * Then, uses this data to build intents for FileListViewActivity and gClassActivity.
     * In the case that a specific json is not available, Toasts the user that the associated
     * service is unavailable.
     */
    fun buildActivitiesFromCache(user: GUser){
        //initialize variables
        val cacheManager = CacheUtility()
        val fileData = cacheManager.getStringFromCache( getString(R.string.fileList), this)
        val classData = cacheManager.getStringFromCache(  getString(R.string.classList), this)


        /**
         * Build Google Drive intent
         */

        //if empty string, no data available
        if( fileData == "")
        {
            //notify user of service disruption
            Toast.makeText(this,
                "No internet or cached data: Google Drive will be unavailable.",
                Toast.LENGTH_LONG).show()
        }

        //else data available
        else {
            //assemble as json object
            val fileList : DigiDrive.DF = Json.decodeFromString(fileData)

            //set call activity intent
            flintent = Intent(this, FileListViewActivity::class.java)
            flintent.putExtra("fileList", fileList)
            flintent.putExtra("guser", user)

            /*
            //bind intent to view files button
            val nextbtn = findViewById<Button>(R.id.btn_pick)
            nextbtn.setOnClickListener() {
                this.startActivity(flintent)
            }
            */
        }


        /**
         * Build Google Class intent
         */
        //if empty string, no data available
        if( classData == "")
        {
            println("CLASS DATA IF ENTERED")
            //notify user of service disruption
            Toast.makeText(this,
                "No internet or cached data: Google Class will be unavailable.",
                Toast.LENGTH_LONG).show()
        }

        //else data available
        else {
            println("CLASS DATA ELSE ENTERED")
            //assemble as json object
            val classData = JSONObject(classData)

            //set call activity intent
            gclassIntent = Intent(this, GClassActivity::class.java)
            gclassIntent.putExtra("classJson", classData.toString())
            gclassIntent.putExtra("gsoData", intent.extras)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }

    // Network connection detector
    override fun onResume() {
        super.onResume()
        networkMonitor.register()
    }

    // Network connection detector
    override fun onStop() {
        super.onStop()
        networkMonitor.unregister()
    }

    private fun dummyDeffered() = scope.async{
        return@async dummy()
    }

    data class dummy( var d: Nothing? = null ) : java.io.Serializable
}