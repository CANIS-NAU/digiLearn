package com.example.loginfordigipack


import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonObjectRequest
import kotlinx.android.synthetic.main.activity_file_list_view.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException


class FileListViewActivity : AppCompatActivity() {
    var filenames = arrayListOf<String>()
    var fileids = arrayListOf<String>()

    var email : String? = null
    var url = getString(R.string.serverUrl).plus("download/goat.jpeg")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_file_list_view)

        read_json()
        write_to_ui_and_listen(filenames)
    }

    // Read the json file and the display it on the activity layout
    fun read_json(){

        try {
            // Read the text file

            var json : String? = intent.getStringExtra("fileListJson")
            var gsodata = intent.getBundleExtra("gsoData")
            println(gsodata?.getString("google_email"))

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
        }catch (e : IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }

    }

    fun write_to_ui_and_listen(fileNames: ArrayList<String>)
    {
        try{
            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, filenames)

            json_info.adapter = adapterView

            // Creates an onclick listener when the user clicks on the driveID that would be referenced to driveID
            json_info.onItemClickListener = AdapterView.OnItemClickListener{
                parent, view, position, id->
                //position is the index of the list item that corresponds to the button clicked
                Toast.makeText(applicationContext, "Type Selected is" + filenames[position],Toast.LENGTH_LONG).show()

                //url should not be global in prod
                //should be created dynamically for the task at hand
                FileDownloader().getFile(this, url)

            }
        }catch(e: IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "FileListViewActivity write_to_ui error: %s".format(e.toString()))
        }
    }

    fun refreshList(queue: RequestQueue, reqMethodCode: Int,request: JSONObject, getFileUrl: String){
        val req = JsonObjectRequest(reqMethodCode, getFileUrl, request,
                { resp ->
                    //do something with a positive response
                },
                { err ->
                    //do something with an error
                }
                )
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        FileDownloader().onRequestPermissionsResult(requestCode, permissions, grantResults)
    }
}
