package com.example.digipack

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.Menu
import android.widget.Toast
import android.view.MenuItem
import android.widget.*
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.activity_details.*
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
        setContentView(R.layout.activity_details)
        flintent = Intent(this, FileListViewActivity::class.java)
        gclassIntent = Intent(this, gClassActivity::class.java)
        gsearchIntent = Intent(this, gSearchActivity::class.java)

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
                            ConnectionType.Wifi -> {
                                clouds.setImageResource(R.drawable.sun_connection)
                                //internet_connection.text = "Wifi Connection"
                                connectToServer()

                            }
                            ConnectionType.Cellular -> {
                                clouds.setImageResource(R.drawable.sun_connection)
                                //internet_connection.text = "Cellular Connection"
                                connectToServer()
                            }
                            else -> { }
                        }
                    }
                    false -> {
                        clouds.setImageResource(R.drawable.networkclouds)
                        //internet_connection.text = "No Connection"
                        connectToServer()
                    }
                }
            }
        }

        // Automatically calls connection to the server
        connectToServer()
    }

    // When menu bar is clicked
    override fun onCreateOptionsMenu(menu: Menu): Boolean {

        // Shows the logo on the action bar
        //supportActionBar?.setLogo(R.drawable.ic_launcher_foreground)
        //supportActionBar?.setDisplayShowHomeEnabled(true)
        //supportActionBar?.setIcon(R.drawable.digipacklogo)
        //supportActionBar?.
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu, menu)
        return true
    }

    // Function to do when items on the menu option are clicked
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        val id = item.getItemId()

        // Fix linking to google drive


        if (id == R.id.googleDriveBtn) {
            // Makes a toast mssg for the user
            Toast.makeText(this, "Google Drive", Toast.LENGTH_LONG).show()
            // Go to the Google Drive page
            startActivity(flintent)

            return true
        }
        if (id == R.id.googleClassBtn) {
            // Makes a toast mssg for the user
            Toast.makeText(this, "Google Classroom Page", Toast.LENGTH_LONG).show()
            // Go to GClass page
            startActivity(gclassIntent)
            return true
        }
        if (id == R.id.googleSearchBtn) {
            // Makes a toast mssg for the user
            Toast.makeText(this, "Google Search Clicked", Toast.LENGTH_LONG).show()
            // Go to GSearch Page
            startActivity(gsearchIntent)

            return true
        }

        return super.onOptionsItemSelected(item)
    }

    private fun connectToServer(){
        val googleId = intent.getStringExtra("google_id")
        val googleFirstName = intent.getStringExtra("google_first_name")
        val googleLastName = intent.getStringExtra("google_last_name")
        val googleEmail = intent.getStringExtra("google_email")
        val googleProfilePicURL = intent.getStringExtra("google_profile_pic_url")
        val googleAccessToken = intent.getStringExtra("google_auth_code")

        // For the debug
        //val mptv = findViewById<TextView>(R.id.mptext)

        val authurl = "auth/"
        val drivelisturl = "drive/$googleEmail"
        val classlisturl = "gclass/$googleEmail"
        val queue = RequestQueueSingleton.getInstance(this.applicationContext)
        val tok = JsauthTok(googleAccessToken, googleEmail)
        val gtok = Gson().toJson(tok)
        val jsobtok = JSONObject(gtok)
        var resp = JSONObject("{Result:noACK}")

        val request = JsonObjectRequest(Request.Method.POST, getString(R.string.serverUrl).plus(authurl), jsobtok,
            { response -> resp = response
                if( resp.get("Result") == "ACK"){
                    val success = "Authentication Successful"
                    //mptv.text = success
                    getFileList(googleFirstName, googleEmail, googleId)
                    getClassList(googleFirstName, googleEmail, googleId)
                }
            },
            { error ->
                //mptv.text = error.toString()
                }
        )
        queue.addToRequestQueue(request)
    }

    private fun getClassList(googleFirstName: String?, googleEmail: String?, googleId: String?){
        val classlisturl = "gclass/$googleEmail"
        val queue = RequestQueueSingleton.getInstance(this.applicationContext)
        val user = Jsuser(googleFirstName, googleEmail, googleId)
        val guser = Gson().toJson(user)
        val jsuserobj = JSONObject(guser)
        var gcresp = JSONObject("{Result:noACK}")
        val gclassRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(classlisturl), jsuserobj,
                { classresp -> gcresp = classresp
                    try{
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
        queue.addToRequestQueue(gclassRequest)
    }

    private fun getFileList(googleFirstName:String?, googleEmail:String?, googleId:String?) {
        val drivelisturl = "drive/$googleEmail"
        val queue = RequestQueueSingleton.getInstance(this.applicationContext)
        val user = Jsuser(googleFirstName, googleEmail, googleId)
        val guser = Gson().toJson(user)
        val jsuserobj = JSONObject(guser)
        var filelistResp = JSONObject("{Result:noACK}")
        val filelistRequest = JsonObjectRequest(Request.Method.GET, getString(R.string.serverUrl).plus(drivelisturl), jsuserobj,
                { flresponse -> filelistResp = flresponse
                    try{
                        Log.i(getString(R.string.app_name), "in details act/getFileList, %s".format(flresponse.toString()))
                        flintent.putExtra("fileListJson", flresponse.toString())
                        flintent.putExtra("gsoData", intent.extras)
                        btn_pick.setOnClickListener{
                            startActivity(flintent)
                        }
                    }catch(e: JSONException){
                        Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
                    }
                },
                { err -> Log.i(getString(R.string.app_name), err.toString())
                    Toast.makeText(applicationContext, err.toString(), Toast.LENGTH_LONG).show()}
        )
        queue.addToRequestQueue(filelistRequest)
    }

    override fun onResume() {
        super.onResume()
        networkMonitor.register()
    }

    override fun onStop() {
        super.onStop()
        networkMonitor.unregister()
    }
}

data class Jsuser(
    @SerializedName("userName")
    var userName: String? = null,
    @SerializedName("googleEmail")
    var email: String? = null,
    @SerializedName("googleId")
    var gid: String? = null
)

data class JsauthTok (
    @SerializedName("googleAccessToken")
    var authToken: String? = null,
    @SerializedName("gooogleEmail")
    var email: String? = null
)