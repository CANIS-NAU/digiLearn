package com.example.loginfordigipack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.activity_details.*
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject

class DetailsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_details)

        //
        val googleId = intent.getStringExtra("google_id")
        val googleFirstName = intent.getStringExtra("google_first_name")
        val googleLastName = intent.getStringExtra("google_last_name")
        val googleEmail = intent.getStringExtra("google_email")
        val googleProfilePicURL = intent.getStringExtra("google_profile_pic_url")
        val googleAccessToken = intent.getStringExtra("google_id_token")

        google_id_textview.text = googleId
        google_first_name_textview.text = googleFirstName
        google_last_name_textview.text = googleLastName
        google_email_textview.text = googleEmail
        google_profile_pic_textview.text = googleProfilePicURL
        google_id_token_textview.text = googleAccessToken

        val mptv = findViewById<TextView>(R.id.mptext)
        val authurl = "http://143.110.158.203:8000/auth/"
        val getlisturl = "http://143.110.158.203:8000/user=$googleEmail"
        val queue = Volley.newRequestQueue(this)
        val tok = JsauthTok(googleAccessToken, googleEmail)
        val gtok = Gson().toJson(tok)
        val jsobtok = JSONObject(gtok)
        var resp = JSONObject("{Result:noACK}")

        val request = JsonObjectRequest(Request.Method.POST, authurl, jsobtok,
            Response.Listener { response -> resp = response },
                Response.ErrorListener { error ->
                    mptv.text = error.toString() }
                )
        queue.add(request)
        println(resp.get("Result"))
        if( resp.get("Result") == "ACK" ){
            val success = "Authentication Successful"
            mptv.text = success
            //and then start the download with GET file list with email
            val user = Jsuser(googleFirstName, googleEmail, googleId)
            val guser = Gson().toJson(user)
            val jsuserobj = JSONObject(guser)

            var filelistResp = JSONObject("{Result:noACK}")

            val filelistRequest = JsonObjectRequest( Request.Method.GET, getlisturl, jsuserobj,
                    Response.Listener { response -> filelistResp = response },
                    Response.ErrorListener { error ->
                        Toast.makeText(applicationContext, error.toString(), Toast.LENGTH_LONG).show()
                    }
                    )
            queue.add(filelistRequest)

            try{
                if(filelistResp.get("my-drive") is JSONArray)
                {
                    //send it to kristine's part
                }
                else{
                    //idfk how the above call didnt throw an error
                }
            } catch (e: JSONException){
                //idk how to handle this so for now...
                Log.e(getString(R.string.app_name), "JSON key error: %s".format(e))
            }
        }
        else
        {
            //handle this some how
            Log.e(getString(R.string.app_name), "Something broke real bad in the details activity")
        }

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