package com.example.digipack

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import kotlinx.android.synthetic.main.activity_details.*

class change_ui_activity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_change_ui)

        val googleFirstName = intent.getStringExtra("google_first_name")
        google_first_name_textview.text = googleFirstName

        // Looking for the file button connection
        val kidUIBttn = findViewById<Button>(R.id.kid_ui_bttn)
        val youngAdultBttn = findViewById<Button>(R.id.youngAdult_ui_bttn_)


        kidUIBttn.setOnClickListener{
            //get the account the user signed in with
            val account = GoogleSignIn.getLastSignedInAccount(this)

            //if the user already signed in
            if(account != null )
            {
                //extract profile information, ID token
                val googleEmail = account.email
                val googleFirstName = account.givenName
                val googleLastName = account.familyName
                val googleProfilePicURL = account.photoUrl.toString()
                val googleIdToken = account.idToken
                val googleId = account.id

                //construct and start intent for Details activity
                val myIntent = Intent(this, kid_main_page::class.java)

                myIntent.putExtra("google_id", googleId)
                myIntent.putExtra("google_first_name", googleFirstName)
                myIntent.putExtra("google_last_name", googleLastName)
                myIntent.putExtra("google_email", googleEmail)
                myIntent.putExtra("google_profile_pic_url", googleProfilePicURL)
                myIntent.putExtra("google_auth_code", googleIdToken)
                myIntent.putExtra("firstSignIn", false)

                this.startActivity(myIntent)
            }
        }

        youngAdultBttn.setOnClickListener{
            //get the account the user signed in with
            val account = GoogleSignIn.getLastSignedInAccount(this)

            //if the user already signed in
            if(account != null )
            {
                //extract profile information, ID token
                val googleEmail = account.email
                val googleFirstName = account.givenName
                val googleLastName = account.familyName
                val googleProfilePicURL = account.photoUrl.toString()
                val googleIdToken = account.idToken
                val googleId = account.id

                //construct and start intent for Details activity
                val myIntent = Intent(this, DetailsActivity::class.java)

                myIntent.putExtra("google_id", googleId)
                myIntent.putExtra("google_first_name", googleFirstName)
                myIntent.putExtra("google_last_name", googleLastName)
                myIntent.putExtra("google_email", googleEmail)
                myIntent.putExtra("google_profile_pic_url", googleProfilePicURL)
                myIntent.putExtra("google_auth_code", googleIdToken)
                myIntent.putExtra("firstSignIn", false)

                this.startActivity(myIntent)
            }
        }

    }
}
