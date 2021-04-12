package com.example.digipack



import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.Menu
import android.widget.Toast
import android.view.MenuItem
import android.widget.Button
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.activity_details.*
import org.json.JSONException
import org.json.JSONObject

class kid_main_page : AppCompatActivity() {

    // Call the network detector tool
    private val networkMonitor = networkDetectorTool(this)

    private lateinit var flintent : Intent
    private lateinit var gclassIntent : Intent
    private lateinit var gsearchIntent : Intent

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_kid_main_page)

        gsearchIntent = Intent(this, kids_gSearchActivity::class.java)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>DigiPack</font>");

        val googleId = intent.getStringExtra("google_id")
        val googleFirstName = intent.getStringExtra("google_first_name")
        val googleLastName = intent.getStringExtra("google_last_name")
        val googleEmail = intent.getStringExtra("google_email")
        val googleProfilePicURL = intent.getStringExtra("google_profile_pic_url")
        val googleAccessToken = intent.getStringExtra("google_auth_code")

        google_first_name_textview.text = googleFirstName
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
                                connectToServer()
                            }
                            else -> { }
                        }
                    }
                    false -> {
                        clouds.setImageResource(R.drawable.networkclouds)
                        //internet_connection.text = "No Connection"

                        //build activities from cache
                        buildActivitiesFromCache()
                    }
                }
            }
        }

        // GDrive Button
        val googleDriveButton = findViewById<Button>(R.id.googleDriveBtn)
        googleDriveButton.setOnClickListener{
            startActivity(flintent)
        }

        // GClass Button
        val googleClassButton = findViewById<Button>(R.id.googleClassBtn)
        googleClassButton.setOnClickListener{
            startActivity(gclassIntent)
        }

        // GSearch Button
        val googleSearchButton = findViewById<Button>(R.id.googleSearchBtn)
        googleSearchButton.setOnClickListener{
            startActivity(gsearchIntent)
        }
    }

    //serverAuth handles initial sign-in authentication with the server.
    private fun serverAuth(){
        val googleEmail = intent.getStringExtra("google_email")
        val googleAccessToken = intent.getStringExtra("google_auth_code")

        // For the debug
        //val mptv = findViewById<TextView>(R.id.mptext)

        val authurl = "auth/"
        val queue = RequestQueueSingleton.getInstance(this.applicationContext)
        val tok = DigiJson.JsauthTok(googleAccessToken, googleEmail)
        val gtok = Gson().toJson(tok)
        val jsobtok = JSONObject(gtok)

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
    private fun connectToServer(){
        //need to add something in here to check the server if theres new content and if so then
        //run all the other methods again and reinitialize the intents
        val fso = intent.getBooleanExtra("firstSignIn", true)
        if(fso){
            serverAuth()
        }
        val googleId = intent.getStringExtra("google_id")
        val googleFirstName = intent.getStringExtra("google_first_name")
        val googleEmail = intent.getStringExtra("google_email")
        getFileList(googleFirstName, googleEmail, googleId)
        getClassList(googleFirstName, googleEmail, googleId)
    }

    //helper function for connectToServer handles acquisition of GCLass data
    private fun getClassList(googleFirstName: String?, googleEmail: String?, googleId: String?){
        when{
            this::gclassIntent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: classIntent already initialized")
            }
            else -> {
                val classlisturl = "gclass/$googleEmail"
                val queue = RequestQueueSingleton.getInstance(this.applicationContext)
                val user = DigiJson.Jsuser(googleFirstName, googleEmail, googleId)
                val guser = Gson().toJson(user)
                val jsuserobj = JSONObject(guser)
                var gcresp = JSONObject("{Result:noACK}")
                val gclassRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(classlisturl), jsuserobj,
                        { classresp -> gcresp = classresp
                            try{
                                //get json response as string, pass to CacheUtility
                                val cacheManager = CacheUtility()
                                cacheManager.cacheString(classresp.toString(), getString(R.string.classList), this)

                                //build gclassIntent
                                gclassIntent = Intent(this, kids_gClassActivity::class.java)
                                Log.i(getString(R.string.app_name), "in details act/getClassList, %s".format(gcresp.toString()))
                                gclassIntent.putExtra("classJson", gcresp.toString())
                                gclassIntent.putExtra("gsoData", intent.extras)
                            }catch(e: JSONException){
                                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                            }
                        },
                        {
                            err ->
                            Log.i(getString(R.string.app_name), err.toString())
                            Toast.makeText(applicationContext, err.toString(), Toast.LENGTH_LONG).show()
                        }
                )
                gclassRequest.retryPolicy = DefaultRetryPolicy(10000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
                queue.addToRequestQueue(gclassRequest)
            }
        }
    }

    //helper function for connectToServer handles acquisition of GDrive data
    private fun getFileList(googleFirstName:String?, googleEmail:String?, googleId:String?) {
        when{
            this::flintent.isInitialized -> {
                Log.i(getString(R.string.app_name), "Details_act: flintent already initialized")
            }
            else -> {
                val drivelisturl = "drive/$googleEmail"
                val queue = RequestQueueSingleton.getInstance(this.applicationContext)
                val user = DigiJson.Jsuser(googleFirstName, googleEmail, googleId)
                val guser = Gson().toJson(user)
                val jsuserobj = JSONObject(guser)
                var filelistResp = JSONObject("{Result:noACK}")
                val filelistRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(drivelisturl), jsuserobj,
                        { flresponse -> filelistResp = flresponse
                            try{
                                val cacheManager = CacheUtility()
                                cacheManager.cacheString(flresponse.toString(), getString(R.string.fileList), this)

                                flintent = Intent(this, kids_gDriveFileActivity::class.java)
                                Log.i(getString(R.string.app_name), "in details act/getFileList, %s".format(flresponse.toString()))
                                flintent.putExtra("fileListJson", flresponse.toString())
                                flintent.putExtra("gsoData", intent.extras)

                                /*
                                btn_pick.setOnClickListener{
                                    startActivity(flintent)
                                }
                                */

                            }catch(e: JSONException){
                                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                            }
                        },
                        { err -> Log.i(getString(R.string.app_name), err.toString())
                            Toast.makeText(applicationContext, err.toString(), Toast.LENGTH_LONG).show()}
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
    fun buildActivitiesFromCache(){
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
            val fileList = JSONObject(fileData)

            //set call activity intent
            flintent = Intent(this, kids_gDriveFileActivity::class.java)
            flintent.putExtra("fileListJson", fileList.toString())
            flintent.putExtra("gsoData", intent.extras)

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
            gclassIntent = Intent(this, kids_gClassActivity::class.java)
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