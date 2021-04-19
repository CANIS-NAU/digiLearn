package com.example.digipack

import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import kotlinx.android.synthetic.main.activity_details.*


/**
 * Change_ui_activity determines what ui to show to the users.
 */
class change_ui_activity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_change_ui)

        val guser = intent.getSerializableExtra("guser") as GUser
        val fso = intent.getBooleanExtra("firstSignIn", true)
        val account = GoogleSignIn.getLastSignedInAccount(this)
        google_first_name_textview.text = guser.firstName

        // Looking for the file button connection
        val kidUIBttn = findViewById<Button>(R.id.kid_ui_bttn)
        val youngAdultBttn = findViewById<Button>(R.id.youngAdult_ui_bttn_)


        kidUIBttn.setOnClickListener{
            onclick(guser, true, fso)
        }

        youngAdultBttn.setOnClickListener{
            onclick(guser, false, fso)
        }
    }


    /**
     * Function Name: onClick
     * Algorithm: Takes the user info, and ui boolean. It determines the next page activity and
     * also output the intents
     *
     * Arguments:
     *     ui - Boolean betwween the UIs
     *     guser - Json Object
     *     fso - ?
     */
    private fun onclick(guser: GUser, ui: Boolean, fso: Boolean){
        //construct and start intent for Details activity
        val myIntent = Intent(this, DetailsActivity::class.java)

        myIntent.putExtra("guser", guser)
        myIntent.putExtra("firstSignIn", fso)
        myIntent.putExtra("ui", ui)

        this.startActivity(myIntent)
    }
}
