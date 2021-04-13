package com.example.digipack

import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.Scopes
import com.google.android.gms.common.api.ApiException
import com.google.android.gms.common.api.Scope
import com.google.android.gms.tasks.Task
import kotlinx.android.synthetic.main.activity_main.*

//results codes
private const val RC_SIGN_IN = 100
private const val EXPLICIT_SIGN_IN = 201
private const val IMPLICIT_SIGN_IN = 202


class MainActivity : AppCompatActivity() {

    lateinit var mGoogleSignInClient: GoogleSignInClient

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        //initialize google sign in object
        val gso =
                GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                        .requestEmail()
                        .requestIdToken(getString(R.string.serverClientId))
                        .requestScopes(Scope(Scopes.DRIVE_FULL),
                                Scope("https://www.googleapis.com/auth/classroom.courses"),
                                Scope("https://www.googleapis.com/auth/classroom.coursework.me"),
                                Scope("https://www.googleapis.com/auth/classroom.announcements"),
                                Scope("https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly"))
                        .requestServerAuthCode(getString(R.string.serverClientId))
                        .build()

        mGoogleSignInClient = GoogleSignIn.getClient(this, gso)

        google_sign_in_button.setOnClickListener {
            signIn()
        }

        //silent sign in operation gets new id token
        mGoogleSignInClient.silentSignIn()
                .addOnCompleteListener( this) { task -> handleSignInResult(task, IMPLICIT_SIGN_IN) }
    }

        //sign in function for the google sign in button
    private fun signIn() {
        val userSignInIntent = mGoogleSignInClient.signInIntent
        startActivityForResult(
                userSignInIntent, RC_SIGN_IN //Passes result to onActivityResult
        )
    }

    // Checks if the requestCode is the same, if so then continue the sign in process
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        //if block handled activityResult for signIn
        if (requestCode == RC_SIGN_IN) {
            val task =
                    GoogleSignIn.getSignedInAccountFromIntent(data)
            handleSignInResult(task, EXPLICIT_SIGN_IN) //passes task to handleSignInResult
        }
    }

    // The user is signed in successfully and will get the user's basic info
    private fun handleSignInResult(completedTask: Task<GoogleSignInAccount>, resultCode: Int) {
        try {
            println("handle sign in entered")
            val userAccount = completedTask.getResult(
                    ApiException::class.java
            )
            println("user account value obtained")

            // Signed in successfully, extract progile information
            val googleId = userAccount?.id ?: ""
            Log.i("Google ID", googleId)

            val googleFirstName = userAccount?.givenName ?: ""
            Log.i("Google First Name", googleFirstName)

            val googleLastName = userAccount?.familyName ?: ""
            Log.i("Google Last Name", googleLastName)

            val googleEmail = userAccount?.email ?: ""
            Log.i("Google Email", googleEmail)

            val idToken = userAccount?.idToken ?: ""
            Log.i("Google ID Token", idToken)
            println("Google idToken " + idToken)

            val authCode = userAccount?.serverAuthCode ?: "" //auth code used for registration with server
            Log.i("Google Auth Code", authCode)

            // construct and launch an intent for DetailsActivity
            val myIntent = Intent(this, change_ui_activity::class.java)
            val guser = GUser( googleId, googleFirstName, googleLastName, googleEmail, authCode, idToken )
            myIntent.putExtra("guser", guser)

            //check if silent sign in
            if(resultCode == IMPLICIT_SIGN_IN)
            {
                //then record NOT first sign in
                myIntent.putExtra("firstSignIn", false)
            }
            //else check if explicit sign in
            else if( resultCode == EXPLICIT_SIGN_IN)
            {
                //then record as first sign in
                myIntent.putExtra("firstSignIn", true)
            }

            this.startActivity(myIntent)

        } catch (e: ApiException) {
            // Checks if the sign in is unsuccessful, if not then throws an error code
            Log.e(
                    "failed code=", e.statusCode.toString()
            )
        }
    }

}