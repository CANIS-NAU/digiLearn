 package com.example.digipack



import DigiJson.DigiClass
import DigiJson.DigiDrive
import DigiJson.DigiSearch
import DigiJson.DigiUser
import DigiJson.GUserJson.GUser
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.Menu
import android.widget.Toast
import android.view.MenuItem
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_details.*
import kotlinx.android.synthetic.main.activity_details.clouds
import kotlinx.android.synthetic.main.activity_details.google_first_name_textview
import kotlinx.android.synthetic.main.activity_kid_main_page.*
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.encodeToJsonElement
import org.json.JSONException
import org.json.JSONObject

class DetailsActivity : AppCompatActivity() {

    // Call the network detector tool
    private val networkMonitor = networkDetectorTool(this)

    private lateinit var flintent : Intent
    private lateinit var gclassIntent : Intent
    private lateinit var gsearchIntent : Intent

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val ui = intent.getBooleanExtra("ui", false)

        if(ui){
            setContentView(R.layout.activity_kid_main_page)
        }else{
            setContentView(R.layout.activity_details)
        }

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>DigiPack</font>");

        val guser = intent.getSerializableExtra("guser") as GUser

        google_first_name_textview.text = guser.firstName
        //google_email_textview.text = googleEmail

        // Calls the network detector class
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
                                connectToServer(guser, ui)
                            }
                            else -> { }
                        }
                    }
                    false -> {
                        clouds.setImageResource(R.drawable.networkclouds)
                        //internet_connection.text = "No Connection"

                        //build activities from cache
                        buildActivitiesFromCache(guser, ui)
                    }
                }
            }
        }

        // GDrive Button
        googleDriveBtn?.setOnClickListener {
            when{
                this::flintent.isInitialized -> startActivity(flintent)
                else ->{  //google drive intent not initialized; block activity and report unavailable
                    Toast.makeText(this, "Google Drive not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
        }

        // GClass Button
        googleClassBtn?.setOnClickListener{
            when{  //google class intent not initialized; block activity and report unavailable
                this::gclassIntent.isInitialized -> startActivity(gclassIntent)
                else ->{
                    Toast.makeText(this, "Google Classroom not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
        }

        // GSearch Button
        googleSearchBtn?.setOnClickListener{
            when{
                this::gsearchIntent.isInitialized -> startActivity(gsearchIntent)
                else ->{
                    Toast.makeText(this, "Google Search not available, check again later", Toast.LENGTH_SHORT).show()
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
        val id = item.getItemId()

        //case google drive button
        if (id == R.id.googleDriveBtn) {
            // Makes a toast mssg for the user
            //Toast.makeText(this, "Google Drive", Toast.LENGTH_LONG).show()
            // Go to the Google Drive page
            when{
                this::flintent.isInitialized -> startActivity(flintent)
                else ->{  //google drive intent not initialized; block activity and report unavailable
                    Toast.makeText(this, "Google Drive not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }

            return true
        }

        // case google class button
        if (id == R.id.googleClassBtn) {
            // Makes a toast mssg for the user
            //Toast.makeText(this, "Google Classroom Page", Toast.LENGTH_LONG).show()
            // Go to GClass page
            when{  //google class intent not initialized; block activity and report unavailable
                this::gclassIntent.isInitialized -> startActivity(gclassIntent)
                else ->{
                    Toast.makeText(this, "Google Classroom not available, check again later", Toast.LENGTH_SHORT).show()
                }
            }
            return true
        }

        //case google search button
        if (id == R.id.googleSearchBtn) {
            // Makes a toast mssg for the user
            //Toast.makeText(this, "Google Search Clicked", Toast.LENGTH_LONG).show()
            // Go to GSearch Page
            when{
                this::gsearchIntent.isInitialized -> startActivity(gsearchIntent)
            }

            return true
        }

        return super.onOptionsItemSelected(item)
    }


    //serverAuth handles initial sign-in authentication with the server.
    private fun serverAuth(guser: GUser){
        val googleEmail = guser.email
        val googleAccessToken = guser.authCode

        println( googleAccessToken?:"")
        // For the debug
        //val mptv = findViewById<TextView>(R.id.mptext)

        val authurl = "auth/"
        val queue = RequestQueueSingleton.getInstance(this.applicationContext)
        val tok = Json.encodeToString(DigiUser.JsauthTok(googleAccessToken, googleEmail))
        println( tok?:"")
        val jsobtok = JSONObject(tok)

        val request = JsonObjectRequest(Request.Method.POST, getString(R.string.serverUrl).plus(authurl), jsobtok,
                { response ->
                    if( response.get("Result") == "ACK"){
                        val success = "Authentication Successful"
                        //mptv.text = success
                    }
                },
                { error ->
                    //mptv.text = error.toString()
                }
        )
        queue.addToRequestQueue(request)
    }

    //Retrieves and caches initial data from the server
    //including: GDrive data, GClass data
    private fun connectToServer(guser: GUser, ui: Boolean){
        //need to add something in here to check the server if theres new content and if so then
        //run all the other methods again and reinitialize the intents
        val fso = intent.getBooleanExtra("firstSignIn", true)
        if(fso){
            serverAuth(guser)
        }

        getFileList(guser, ui)
        getClassList(guser, ui)
        //getSearchList(guser)
    }

    private fun getSearchList(guser: GUser, ui: Boolean){
        when{
            this::gsearchIntent.isInitialized ->{
                Log.i(getString(R.string.app_name), "Details_act: searchIntent already initialized")
            }
            else -> {
                val searchlisturl = "search/${guser.idToken}"
                val queue = RequestQueueSingleton.getInstance(this.applicationContext)
                val user = DigiUser.Jsuser(guser.firstName, guser.email, guser.idToken)
                val jsuserobj = JSONObject(Json.encodeToString(user))
                var gsresp = JSONObject("{Result:noACK}")

                val gsearchrequest = JsonObjectRequest( Request.Method.GET, getString(R.string.serverUrl).plus(searchlisturl), jsuserobj,
                        { searchresp -> gsresp = searchresp
                            try{
                                if(gsresp == JSONObject("{Result:noACK}")){
                                    Toast.makeText(applicationContext, "noACK for getSearchList", Toast.LENGTH_SHORT).show()
                                }else{
                                    //get json response as string, pass to CacheUtility
                                    val cacheManager = CacheUtility()
                                    val searchJson : DigiSearch.DigiRes = Json.decodeFromString(gsresp.toString())

                                    cacheManager.cacheString(gsresp.toString(), getString(R.string.searchList), this)
                                    gsearchIntent = Intent(this, gSearchActivity::class.java)
                                    gsearchIntent.putExtra("searchlist", searchJson)
                                    gsearchIntent.putExtra("guser", guser)
                                    gsearchIntent.putExtra("ui", ui)
                                }
                            }catch(e: JSONException){
                                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                            }
                        },
                        { err -> Log.i(getString(R.string.app_name), err.toString()) }
                        )
                queue.addToRequestQueue(gsearchrequest)
            }
        }
    }

    //helper function for connectToServer handles acquisition of GCLass data
    private fun getClassList(guser: GUser, ui : Boolean){
        when{
            this::gclassIntent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: classIntent already initialized")
            }
            else -> {
                val classlisturl = "gclass/${guser.idToken}"
                val queue = RequestQueueSingleton.getInstance(this.applicationContext)
                val user = DigiUser.Jsuser(guser.firstName, guser.email, guser.idToken)
                val jsuserobj = JSONObject(Json.encodeToString(user))
                println("juser "+ jsuserobj)
                var gcresp = JSONObject("{Result:noACK}")
                val gclassRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(classlisturl), jsuserobj,
                        { classresp -> gcresp = classresp
                            try{
                                if(gcresp == JSONObject("{Result:noACK}"))
                                {
                                    Toast.makeText(applicationContext, "noACK for getClassList", Toast.LENGTH_SHORT).show()
                                }
                                else
                                {
                                    //get json response as string, pass to CacheUtility
                                    val cacheManager = CacheUtility()
                                    val classjson : DigiClass.CourseList = Json.decodeFromString(gcresp.toString())

                                    cacheManager.cacheString(classresp.toString(), getString(R.string.classList), this)

                                    //build gclassIntent
                                    gclassIntent = Intent(this, gClassActivity::class.java)
                                    Log.i(getString(R.string.app_name), "in details act/getClassList, %s".format(gcresp.toString()))
                                    gclassIntent.putExtra("courselist", classjson)
                                    gclassIntent.putExtra("guser", guser)
                                    gclassIntent.putExtra("ui", ui)
                                }

                            }catch(e: JSONException){
                                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                            }
                        },
                        {
                            err ->
                            Log.i(getString(R.string.app_name), err.toString())
                        }
                )
                gclassRequest.retryPolicy = DefaultRetryPolicy(10000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
                queue.addToRequestQueue(gclassRequest)
            }
        }
    }

    //helper function for connectToServer handles acquisition of GDrive data
    private fun getFileList(guser: GUser, ui: Boolean) {
        when{
            this::flintent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: flintent already initialized")
            }
            else -> {
                val drivelisturl = "drive/${guser.idToken}"
                val queue = RequestQueueSingleton.getInstance(this.applicationContext)
                val user = DigiUser.Jsuser(guser.firstName, guser.email, guser.idToken)
                val jsuserobj = JSONObject(Json.encodeToString(user))
                var filelistResp = JSONObject("{Result:noACK}")
                val filelistRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(drivelisturl), jsuserobj,
                        { flresponse -> filelistResp = flresponse
                            try{
                                if(filelistResp == JSONObject("{Result:noACK}"))
                                {
                                    Toast.makeText(applicationContext, "noACK for getFileList", Toast.LENGTH_SHORT).show()
                                }
                                else
                                {
                                    val cacheManager = CacheUtility()
                                    val filelist : DigiDrive.DF = Json.decodeFromString(flresponse.toString())
                                    cacheManager.cacheString(flresponse.toString(), getString(R.string.fileList), this)

                                    flintent = Intent(this, FileListViewActivity::class.java)
                                    Log.i(getString(R.string.app_name), "in details act/getFileList, %s".format(flresponse.toString()))

                                    flintent.putExtra("filelist", filelist)
                                    flintent.putExtra("guser", guser)
                                    flintent.putExtra("ui", ui)
                                }

                            }catch(e: JSONException){
                                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                            }
                        },
                        { err -> Log.i(getString(R.string.app_name), err.toString()) }
                )
                queue.addToRequestQueue(filelistRequest)
            }
        }
    }


    /**
     * When the network is unavailable, attempts to retrieve GClass, GDrive data from cache.
     * Then, uses this data to build intents for FileListViewActivity and gClassActivity.
     * In the case that a specific json is not available, Toasts the user that the associated
     * service is unavailable.
     */
    fun buildActivitiesFromCache(guser: GUser, ui: Boolean){
        //initialize variables
        val cacheManager = CacheUtility()
        val fileData = cacheManager.getStringFromCache( getString(R.string.fileList), this)
        val classData = cacheManager.getStringFromCache(  getString(R.string.classList), this)
        val searchData = cacheManager.getStringFromCache(  getString(R.string.searchList), this)


        //Build Google Drive intent
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
            flintent.putExtra("filelist", fileList)
            flintent.putExtra("guser", guser)
            flintent.putExtra("ui", ui)

            /*
            //bind intent to view files button
            val nextbtn = findViewById<Button>(R.id.btn_pick)
            nextbtn.setOnClickListener() {
                this.startActivity(flintent)
            }
            */
        }

        // Build Google Class intent
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
            val classData : DigiClass.CourseList = Json.decodeFromString(classData)

            //set call activity intent
            gclassIntent = Intent(this, gClassActivity::class.java)
            gclassIntent.putExtra("courselist", classData)
            gclassIntent.putExtra("guser", guser)
            gclassIntent.putExtra("ui", ui)
        }

        if(searchData == ""){
            Toast.makeText(this,
                    "No internet or cached data: Google Search will be unavailable.",
                    Toast.LENGTH_LONG).show()
        }
        else{
            val searchData : DigiSearch.DigiRes = Json.decodeFromString(searchData)
            gsearchIntent = Intent(this, gSearchActivity::class.java)
            gsearchIntent.putExtra("courselist", searchData)
            gsearchIntent.putExtra("guser", guser)
            gsearchIntent.putExtra("ui", ui)
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