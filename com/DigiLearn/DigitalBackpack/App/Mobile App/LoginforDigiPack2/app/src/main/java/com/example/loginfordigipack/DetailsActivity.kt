package com.example.loginfordigipack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_details.*

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
        val url = "http://143.110.158.203:8000/login"
        val queue = Volley.newRequestQueue(this)

        val stringRequest = StringRequest(
                Request.Method.GET, url,
                Response.Listener<String> { response ->
                    mptv.text = "Response is: ${response.substring(0, 500)}"
                },
                Response.ErrorListener { error -> mptv.text = "ERROR: %s".format(error.toString()) },
        )
        queue.add(stringRequest)
    }
}