package com.example.digipack

import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.Scopes
import com.google.android.gms.common.api.ApiException
import com.google.android.gms.common.api.Scope
import com.google.android.gms.tasks.Task
import kotlinx.android.synthetic.main.activity_sign_in.*

class SignInActivity : AppCompatActivity() {
    private val RC_SIGN_IN = 100
    lateinit var gsiclient: GoogleSignInClient
    lateinit var guser : GUser
    lateinit var myintent : Intent


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_in)
        //initialize details activity intent
        myintent = Intent(this, DetailsActivity::class.java)
        //get the signed in user or have them sign in
        getSignedIn()

        when{
            //when we finally have a user signed into the app
            this::guser.isInitialized -> {

                myintent.putExtra("guser", guser)
                this.startActivity(myintent)
            }
            //otherwise wait for sign in
            else -> {
                Toast.makeText(this, "Still signing in", Toast.LENGTH_SHORT).show()
            }
        }
    }

    /**
     * get a signed in user or have them sign in
     * and initialize guser
     */
    private fun getSignedIn(){
        val acc = GoogleSignIn.getLastSignedInAccount(this)
        //if the user is already signed in, get their account info
        if( acc != null){
            //signal that that the user is already registered with the server
            myintent.putExtra("firstSignIn", false)
            //initialize user variable
            guser = GUser(acc.email, acc.givenName, acc.familyName, acc.idToken, acc.id, acc.serverAuthCode)
        }
        //else have them sign in
        signIn()
    }

    /**
     * do sign in flow for new user
     */
    private fun signIn(){
        //create google sign in object with proper scopes
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail()
            .requestIdToken(getString(R.string.serverClientId))
            .requestScopes( Scope (Scopes.DRIVE_FULL),
                Scope ("https://www.googleapis.com/auth/classroom.courses"),
                Scope ("https://www.googleapis.com/auth/classroom.coursework.me"),
                Scope ("https://www.googleapis.com/auth/classroom.announcements"),
                Scope ("https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly") )
            .requestServerAuthCode(getString(R.string.serverClientId), true)
            .build()
        //signal that this is the first sign in of the user
        myintent.putExtra("firstSignIn", true)
        //when the user clicks the sign in button have them sign in and wait for result
        google_sign_in_button.setOnClickListener{
            val userSignInIntent = gsiclient.signInIntent
            startActivityForResult(userSignInIntent, RC_SIGN_IN)
        }
    }

    /**
     * when an activity completes, if it returns a value handle that result
     */
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?){
        super.onActivityResult(requestCode, resultCode, data)
        //if block handled activityResult for signIn
        if (requestCode == RC_SIGN_IN) {
            val task =
                GoogleSignIn.getSignedInAccountFromIntent(data)
            handleSignInResult(task) //passes task to handleSignInResult
        }
    }

    /**
     * function to handle sign in result, builds and initializes guser variable
     */
    private fun handleSignInResult(completedTask: Task<GoogleSignInAccount>) {
        try {
            val userAccount = completedTask.getResult(
                ApiException::class.java
            )
            val googleId = userAccount?.id ?: ""
            val googleFirstName = userAccount?.givenName ?: ""
            val googleLastName = userAccount?.familyName ?: ""
            val googleEmail = userAccount?.email ?: ""
            val googleIdToken = userAccount?.idToken ?: ""
            val googleAuthCode = userAccount?.serverAuthCode ?: ""
            //initialize user variable
            guser = GUser(googleEmail, googleFirstName, googleLastName, googleIdToken, googleId, googleAuthCode)
        }
        catch (e: ApiException) {
            // Checks if the sign in is unsuccessful, if not then throws an error code
            Log.e(
                "${R.string.app_name}: failed code=", e.statusCode.toString()
            )
        }
    }
}