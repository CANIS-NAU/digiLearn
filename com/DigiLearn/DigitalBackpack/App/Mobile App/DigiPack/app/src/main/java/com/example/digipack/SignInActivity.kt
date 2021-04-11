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
import kotlinx.android.synthetic.main.activity_sign_in.*
import kotlinx.coroutines.*

class SignInActivity : AppCompatActivity(){
    private val scope = MainScope()

    lateinit var mGoogleSignInClient: GoogleSignInClient
    private val RC_SIGN_IN = 100

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_in)

        val acc = GoogleSignIn.getLastSignedInAccount(this)


        if(acc != null) {
            var detailsintent = Intent(this, DetailsActivity::class.java)
            var guser = GUser(
                acc.email,
                acc.givenName,
                acc.familyName,
                acc.idToken,
                acc.id,
                acc.serverAuthCode
            )
            detailsintent.putExtra("guser", guser)
            detailsintent.putExtra("firstSignIn", false)
            startActivity(detailsintent)
        }
        else{
            val gso =
                GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                    .requestEmail()
                    .requestIdToken( getString(R.string.serverClientId) )
                    .requestScopes( Scope (Scopes.DRIVE_FULL),
                        Scope ("https://www.googleapis.com/auth/classroom.courses"),
                        Scope ("https://www.googleapis.com/auth/classroom.coursework.me"),
                        Scope ("https://www.googleapis.com/auth/classroom.announcements"),
                        Scope ("https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly") )
                    .requestServerAuthCode( getString(R.string.serverClientId), true)
                    .build()

            mGoogleSignInClient = GoogleSignIn.getClient(this, gso)
            google_sign_in_button.setOnClickListener {
                signIn()
            }
        }
    }

    //sign in function for the google sign in button
    private fun signIn() {
        val userSignInIntent = mGoogleSignInClient.signInIntent
        startActivityForResult(
            userSignInIntent, RC_SIGN_IN //Passes result to onActivityResult
        )
    }

    private fun asyncSignInResult(completedTask: Task<GoogleSignInAccount>) = scope.launch{
        val SIA = this@SignInActivity
        var detailsintent = Intent( SIA, DetailsActivity::class.java)
        asyncHandleSIR(completedTask, detailsintent)
    }

    private suspend fun asyncHandleSIR(completedTask: Task<GoogleSignInAccount>, detailsintent: Intent){
        val SIA = this@SignInActivity
        var guser = withContext(Dispatchers.IO){
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
                return@withContext GUser(googleEmail, googleFirstName, googleLastName, googleIdToken, googleId, googleAuthCode)
            }
            catch (e: ApiException) {
                // Checks if the sign in is unsuccessful, if not then throws an error code
                Log.e(
                    "${R.string.app_name}: failed code=", e.statusCode.toString()
                )
            }
        }
        withContext(Dispatchers.Main){
            detailsintent.putExtra("guser", guser)
            detailsintent.putExtra("firstSignIn", true)
            SIA.startActivity(detailsintent)
        }
    }


    // Checks if the requestCode is the same, if so then continue the sign in process
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        //if block handled activityResult for signIn
        if (requestCode == RC_SIGN_IN) {
            val task = GoogleSignIn.getSignedInAccountFromIntent(data)
            //handleSignInResult(task) //passes task to handleSignInResult
            //possibly new improved version with threads
            asyncSignInResult(task)
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
            //return GUser(googleEmail, googleFirstName, googleLastName, googleIdToken, googleId, googleAuthCode)
        }
        catch (e: ApiException) {
            // Checks if the sign in is unsuccessful, if not then throws an error code
            Log.e(
                "${R.string.app_name}: failed code=", e.statusCode.toString()
            )
        }
    }

}


