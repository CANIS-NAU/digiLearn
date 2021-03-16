package com.example.loginfordigipack

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
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
        setContentView(R.layout.activity_main)

        read_json()
    }

    // Read the json file and the display it on the activity layout
    fun read_json(){

        var json : String? = null
        try {
            // Read the text file

            json = intent.getStringExtra("fileListJson")

            // Prints the Json File
            //json_info.text = json

            // Creates an JSON array which will contain data from our Json file
            var jsonArray = JSONObject(json).getJSONArray("File Data")

            // Loop through the json array
            for (i in 0..jsonArray.length()-1){
                // Create a json object to access each value in the file
                var jsonObj =  jsonArray.getJSONObject(i)

                // Array to store the jsonObject
                strInfo.add(jsonObj.getString("fileName"))
            }

            // To display in the ListView
            var adapterView = ArrayAdapter(this,android.R.layout.simple_list_item_1,strInfo)

            json_info.adapter = adapterView

            // Creates an onclick listener when the user clicks on the driveID that would be referenced to driveID
            json_info.onItemClickListener = AdapterView.OnItemClickListener{
                    parent, view, position, id->
                Toast.makeText(applicationContext, "Type Selected is" + strInfo[position],Toast.LENGTH_LONG).show()
            }
        } catch (e : IOException){
            //handle errors eventually
        }

    }
}
