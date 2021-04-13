package com.example.digipack

import DigiJson.GUserJson.GUser
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

        val guser = intent.getSerializableExtra("guser") as GUser
        val fso = intent.getBooleanExtra("firstSignIn", true)
        google_first_name_textview.text = guser.firstName

        // Looking for the file button connection
        val kidUIBttn = findViewById<Button>(R.id.kid_ui_bttn)
        val youngAdultBttn = findViewById<Button>(R.id.youngAdult_ui_bttn_)


        kidUIBttn.setOnClickListener{
            //get the account the user signed in with
            val account = GoogleSignIn.getLastSignedInAccount(this)

            //if the user already signed in
            if(account != null )
            {

                //construct and start intent for Details activity
                val myIntent = Intent(this, DetailsActivity::class.java)

                myIntent.putExtra("guser", guser)
                myIntent.putExtra("firstSignIn", fso)
                myIntent.putExtra("uiSelect", true)

                this.startActivity(myIntent)
            }
        }

        youngAdultBttn.setOnClickListener{
            //get the account the user signed in with
            val account = GoogleSignIn.getLastSignedInAccount(this)

            //if the user already signed in
            if(account != null )
            {
                //construct and start intent for Details activity
                val myIntent = Intent(this, DetailsActivity::class.java)

                myIntent.putExtra("guser", guser)
                myIntent.putExtra("firstSignIn", fso)
                myIntent.putExtra("uiSelect", false)
                this.startActivity(myIntent)
            }
        }

    }
}
