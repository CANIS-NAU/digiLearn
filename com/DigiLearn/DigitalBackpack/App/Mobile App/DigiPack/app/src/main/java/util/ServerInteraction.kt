package util

import DigiJson.DigiClass
import DigiJson.DigiDrive
import DigiJson.DigiServer
import DigiJson.GUserJson.GUser
import DigiJson.DigiUser
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.DefaultRetryPolicy
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.example.digipack.R
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.json.JSONObject

class ServerInteraction {

    lateinit var drivelist : DigiDrive.DF
    lateinit var courselist : DigiClass.CourseList
    lateinit var authsucc : DigiServer.succ
    lateinit var reqfilesucc : DigiServer.succ

    fun isDriveListInitialized(): Boolean {
        return this::drivelist.isInitialized
    }
    fun isCourseListInitialized(): Boolean {
        return this::courselist.isInitialized
    }
    fun isAuthSuccInitialized() : Boolean {
        return this::authsucc.isInitialized
    }
    fun isReqFileSuccInitialized() : Boolean {
        return this::reqfilesucc.isInitialized
    }

    fun auth(user: GUser, activity: AppCompatActivity) : Boolean {
        val googleEmail = user.email
        val googleAccessToken = user.authCode

        val queue = RequestQueueSingleton.getInstance(activity.applicationContext)
        val tok = DigiUser.JsauthTok(googleAccessToken, googleEmail)
        val jsobtok = JSONObject(Json.encodeToString(tok))
        var authurl = activity.getString(R.string.serverUrl)
        authurl.plus(activity.getString(R.string.authUrl))
        val request = JsonObjectRequest(
            Request.Method.POST, authurl, jsobtok,
            { response ->
                if( response.get("Result") == "ACK"){
                    authsucc = DigiServer.succ(1)
                }
            },
            { _ ->
                //
                authsucc = DigiServer.succ(0)
            }
        )
        queue.addToRequestQueue(request)
        return when{
            this::authsucc.isInitialized -> true
            else -> false
        }
    }

    fun getFileList(user: GUser, activity: AppCompatActivity): DigiDrive.DF? {

        //initialization
        val drivelisturl = activity.getString(R.string.serverUrl)
        drivelisturl.plus(activity.getString(R.string.driveUrl)) //just calling it now this might cause issues
        drivelisturl.plus(user.email)
        val queue = RequestQueueSingleton.getInstance(activity.applicationContext)
        val userJson = DigiUser.Jsuser(user.firstName, user.email, user.idToken) //this might need to be userID instead
        val jsuserobj = JSONObject(Json.encodeToString(userJson))

        //send request to server to get file list
        val fileListRequest = JsonObjectRequest(Request.Method.GET, drivelisturl, jsuserobj,
            { flresp ->
                drivelist = Json.decodeFromString(flresp.toString())
            },
            { err ->
                //
                Log.i(activity.getString(R.string.app_name), err.toString())
            }
        )
        //add the request to the queue
        queue.addToRequestQueue(fileListRequest)
        //this might cause issues with just always returning null... idk yet tho.
        return when{
            this::drivelist.isInitialized -> drivelist
            else -> null
        }
    }

    fun getClassList(user: GUser, activity: AppCompatActivity): DigiClass.CourseList? {

        //initialization
        val clistUrl = activity.getString(R.string.serverUrl)
        clistUrl.plus(activity.getString(R.string.classUrl))
        clistUrl.plus(user.email)
        val queue = RequestQueueSingleton.getInstance(activity.applicationContext)
        val userJson = DigiUser.Jsuser(user.firstName, user.email, user.idToken) //this might need to be userID instead
        val jsuserobj = JSONObject(Json.encodeToString(userJson))

        //send request to server to get class list
        val gclassRequest = JsonObjectRequest(Request.Method.GET, clistUrl, jsuserobj,
            { classresp ->
                courselist = Json.decodeFromString(classresp.toString())
            },
            { err ->
                //
                Log.i(activity.getString(R.string.app_name), err.toString())
            }
        )
        //for some reason the server takes a while to respond to the class list request so
        //i extend the retry time a bit here
        gclassRequest.retryPolicy = DefaultRetryPolicy(20000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
        //add the request to the queue
        queue.addToRequestQueue(gclassRequest)
        //this might cause issues with just always returning null... idk yet tho.
        return when{
            this::courselist.isInitialized -> courselist
            else -> null
        }
    }

    fun requestFileForDownload(user: GUser, filedata: DigiDrive.DigiFile, activity: AppCompatActivity) : Boolean{
        val queue = RequestQueueSingleton.getInstance(activity.applicationContext)
        val email = user.email
        val fileid = filedata.fileid
        val reqMethodCode = Request.Method.GET
        val getFileUrl = activity.getString(R.string.serverUrl).plus("sd/${email}/${fileid}")
        val usr = DigiUser.Jsuser(user.firstName, email, user.userID) //this id might be the wrong one

        val reqjson = JSONObject( Json.encodeToString(usr) )

        val req = JsonObjectRequest(reqMethodCode, getFileUrl, reqjson,
            { _ ->

                reqfilesucc.success = 1
            },
            { _ ->

                reqfilesucc.success = 0
            }
        )
        queue.addToRequestQueue(req)
        return when{
            this::reqfilesucc.isInitialized -> true
            else -> false
        }
    }


}