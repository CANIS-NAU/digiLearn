package com.example.loginfordigipack

import android.Manifest
import android.annotation.TargetApi
import android.app.AlertDialog
import android.app.DownloadManager
import android.content.Context
import android.content.pm.PackageManager
import android.database.Cursor
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.android.synthetic.main.activity_file_list_view.*
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.io.InputStream


class FileListViewActivity : AppCompatActivity() {
    var filenames = arrayListOf<String>()
    var fileids = arrayListOf<String>()

    var msg: String? = null
    var lastMsg = ""

    var email : String? = null
    var url = "http://143.110.158.203:8000/download/lion.png"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_file_list_view)

        read_json()
    }

    // Read the json file and the display it on the activity layout
    fun read_json(){

        try {
            // Read the text file

            var json : String? = intent.getStringExtra("fileListJson")

            // Prints the Json File
            //json_info.text = json
            var jsonobj = JSONObject(json)
            Log.i(getString(R.string.app_name), "filelistview jsonobj: %s".format(jsonobj.toString()))

            // Creates an JSON array which will contain data from our Json file
            var jsonArray = JSONArray(jsonobj.getString("Files"))
            Log.i(getString(R.string.app_name), "filelistview jsonArray: %s".format(jsonArray.toString()))
            //Log.i(getString(R.string.app_name), "Json Array: %s".format(internalJsonobj.toString()))

            //var jsonArray = JSONArray(internalJsonobj)
            Log.i(getString(R.string.app_name), "just before the fore loop")
            // Loop through the json array

            for (i in 0..(jsonArray.length() - 1)){
                // Create a json object to access each value in the file
                var jsonObj =  jsonArray.getJSONObject(i)

                // Array to store the jsonObject
                filenames.add(jsonObj.getString("fileName"))
                fileids.add(jsonObj.getString("fileid"))
            }

            // To display in the ListView
            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, filenames)

            json_info.adapter = adapterView

            // Creates an onclick listener when the user clicks on the driveID that would be referenced to driveID
            json_info.onItemClickListener = AdapterView.OnItemClickListener{
                    parent, view, position, id->
                //Log.i(getString(R.string.app_name), "Json Array: %s".format(jsonArray.toString()))
                Toast.makeText(applicationContext, "Type Selected is" + filenames[position],Toast.LENGTH_LONG).show()

                //filenames[position])

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
                    askPermissions()
                } else {
                    downloadFile(url)
                }

            }
        } catch (e : IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }

    }

    private fun downloadFile(url: String){
        val dir = File(Environment.DIRECTORY_DOWNLOADS)

        if(!dir.exists()){
            dir.mkdirs()
        }

        val downloadManager = this.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager

        val downloadUri = Uri.parse(url)

        val request = DownloadManager.Request(downloadUri).apply{
            setAllowedNetworkTypes(DownloadManager.Request.NETWORK_WIFI or DownloadManager.Request.NETWORK_MOBILE)
                    .setAllowedOverRoaming(false)
                    .setTitle(url.substring(url.lastIndexOf("/")+1))
                    .setDescription("")
                    .setDestinationInExternalPublicDir(
                            dir.toString(),
                            url.substring(url.lastIndexOf("/")+1)
                    )
        }

        val downloadId = downloadManager.enqueue(request)
        val query = DownloadManager.Query().setFilterById(downloadId)

        Thread( Runnable {
            var downloading = true
            while(downloading){
                val cursor: Cursor = downloadManager.query(query)
                cursor.moveToFirst()
                if(cursor.getInt(cursor.getColumnIndex(DownloadManager.COLUMN_STATUS)) == DownloadManager.STATUS_SUCCESSFUL) {
                    downloading = false
                }
                val status = cursor.getInt(cursor.getColumnIndex(DownloadManager.COLUMN_STATUS))
                msg = statusMessage( url, dir, status )
                if( msg != lastMsg )
                {
                    this.runOnUiThread{
                        Toast.makeText(this, msg, Toast.LENGTH_SHORT).show()
                    }
                    lastMsg = msg?:""
                }
                cursor.close()
            }
        }).start()
    }

    private fun statusMessage(url: String, directory: File, status: Int): String?{
        var msg = ""
        msg = when( status ){
            DownloadManager.STATUS_FAILED -> "Download has been failed, please try again"
            DownloadManager.STATUS_PAUSED -> "Paused"
            DownloadManager.STATUS_PENDING -> "Pending"
            DownloadManager.STATUS_RUNNING -> "Downloading..."
            DownloadManager.STATUS_SUCCESSFUL -> "Downloaded successfully in $directory" + File.separator + url.substring(
                url.lastIndexOf("/") + 1
            )
            else -> "There's nothing to download"
        }
        return msg
    }

    @TargetApi(Build.VERSION_CODES.M)
    fun askPermissions(){
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.
                AlertDialog.Builder(this)
                    .setTitle("Permission required")
                    .setMessage("Permission required to save photos from the Web.")
                    .setPositiveButton("Accept") { dialog, id ->
                        ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE)
                        finish()
                    }
                    .setNegativeButton("Deny") { dialog, id -> dialog.cancel() }
                    .show()
            } else {
                // No explanation needed, we can request the permission.
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE)
                // MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE is an
                // app-defined int constant. The callback method gets the
                // result of the request.

            }
        } else {
            // Permission has already been granted*********
            downloadFile(url)
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE -> {
                // If request is cancelled, the result arrays are empty.
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    // permission was granted, yay!
                    // Download the Image
                    downloadFile(url)
                } else {
                    // permission denied, boo! Disable the
                    // functionality that depends on this permission.

                }
                return
            }
            // Add other 'when' lines to check for other
            // permissions this app might request.
            else -> {
                // Ignore all other requests.
            }
        }
    }

    companion object{
        private const val MY_PERMISSIONS_REQUEST_WRITE_EXTERNAL_STORAGE = 1
    }
}
