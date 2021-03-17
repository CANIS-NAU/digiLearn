package com.example.loginfordigipack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_file_list_view.*
import kotlinx.android.synthetic.main.activity_main.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.io.InputStream


class FileListViewActivity : AppCompatActivity() {
    var strInfo = arrayListOf<String>()

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

            // Creates an JSON array which will contain data from our Json file
            var jsonArray = JSONArray(jsonobj.getJSONArray("Files"))

            Log.i(getString(R.string.app_name), "Json Array: %s".format(jsonArray.toString()))

            // Loop through the json array
            for (i in 0 until (jsonArray.length() - 1)){
                // Create a json object to access each value in the file
                var jsonObj =  jsonArray.getJSONObject(i)

                // Array to store the jsonObject
                strInfo.add(jsonObj.getString("fileName"))
            }

            // To display in the ListView
            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, strInfo)

            json_info.adapter = adapterView

            // Creates an onclick listener when the user clicks on the driveID that would be referenced to driveID
            json_info.onItemClickListener = AdapterView.OnItemClickListener{
                    parent, view, position, id->
                Log.i(getString(R.string.app_name), "Json Array: %s".format(jsonArray.toString()))
                Toast.makeText(applicationContext, "Type Selected is" + strInfo[position],Toast.LENGTH_LONG).show()
            }
        } catch (e : IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }

    }
}
