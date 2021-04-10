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
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import org.json.JSONObject
import util.CacheUtility
import util.ConnectionType
import util.ServerInteraction
import util.networkDetectorTool

class DetailsActivity : AppCompatActivity() {
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
        networkMonitor.result = { isAvailable, type ->
            runOnUiThread {
                when (isAvailable) {
                    true -> {
                        when (type) {
                            //changed this to only call the server once since we dont care what type
                            //of connection is happening currently
                            ConnectionType.Wifi, ConnectionType.Cellular  -> {
                                clouds.setImageResource(R.drawable.sun_connection)
                                //internet_connection.text = "Wifi Connection"
                                connectToServer(guser)
                            }
                            else -> { }
                        }
                    }
                    false -> {
                        clouds.setImageResource(R.drawable.networkclouds)
                        //internet_connection.text = "No Connection"

                        //build activities from cache
                        buildActivitiesFromCache(guser)
                    }
                }
            }
        }
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

    /**
     * handles connection to server
     * checks if specified intent is intialized and if not initializes it with data from server
     */
    private fun connectToServer(guser: GUser){
        val fso = intent.getBooleanExtra("firstSignIn", true)
        val server = ServerInteraction()
        if(fso){
            server.auth(guser, this)
        }
        //file list flow
        when{
            this::flintent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: file list intent already initialized")
            }
            else -> {
                //send request to server
                var filelist = server.getFileList(guser, this)
                when{
                    server.isDriveListInitialized() -> {
                        flintent = Intent(this, FileListViewActivity::class.java)
                        flintent.putExtra("fileList", filelist)
                        flintent.putExtra("guser", guser)
                    }
                    else -> {
                        Toast.makeText(this, "Loading File List", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }

        //gclass flow
        when{
            this::gclassIntent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: classIntent already initialized")
            }
            else -> {
                //send request to server
                var courselist = server.getClassList(guser, this)
                when{
                    server.isCourseListInitialized() -> {
                        gclassIntent = Intent(this, GClassActivity::class.java)
                        gclassIntent.putExtra("classJson", courselist)
                        gclassIntent.putExtra("guser", guser)
                    }
                    else -> {
                        Toast.makeText(this, "Loading Course List", Toast.LENGTH_SHORT).show()
                    }
                }
            }
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
}