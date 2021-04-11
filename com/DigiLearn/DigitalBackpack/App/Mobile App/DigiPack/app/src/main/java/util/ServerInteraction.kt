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
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.json.JSONObject
import kotlin.coroutines.resume
import kotlin.coroutines.suspendCoroutine

class ServerInteraction(var activity: AppCompatActivity, var scope: CoroutineScope) {


    suspend fun getFileList(user: GUser) = suspendCoroutine<DigiDrive.DF?> { cont ->

        //initialization
        val drivelisturl = activity.getString(R.string.serverUrl).plus(activity.getString(R.string.driveUrl)).plus(user.email)
        val queue = RequestQueueSingleton.getInstance(activity.applicationContext)
        val userJson = DigiUser.Jsuser(user.firstName, user.email, user.idToken) //this might need to be userID instead
        val jsuserobj = JSONObject(Json.encodeToString(userJson))

        //send request to server to get file list
        val fileListRequest = JsonObjectRequest(Request.Method.GET, drivelisturl, jsuserobj,
            { flresp ->
                cont.resume( Json.decodeFromString(flresp.toString()) )
            },
            { err ->
                //
                Log.i(activity.getString(R.string.app_name), "getFileList err: ${err.toString()}")
                cont.resume(null)
            }
        )
        //add the request to the queue
        queue.addToRequestQueue(fileListRequest)
        //this might cause issues with just always returning null... idk yet tho.
    }

}