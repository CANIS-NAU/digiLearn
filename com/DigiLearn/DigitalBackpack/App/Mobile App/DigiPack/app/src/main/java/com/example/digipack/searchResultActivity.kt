package com.example.digipack

import DigiJson.DigiSearch
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_gclass.clouds
import kotlinx.android.synthetic.main.activity_search_history_details.*
import java.io.IOException

class searchResultActivity : AppCompatActivity(){

    // Call the network detector tool
    private val networkMonitor = networkDetectorTool(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val ui = intent.getBooleanExtra("ui", false)

        // Determines what UI to show to  the user
        if(ui){
            setContentView(R.layout.activity_kid_course_details)
        }else{
            setContentView(R.layout.activity_search_history_details)
        }

        //unpack intent to get course data
        var results = intent.getSerializableExtra("results") as DigiSearch.Results
        //var guser = intent.getSerializableExtra("guser") as GUser
        Log.i(getString(R.string.app_name), results.toString())

        // Change title
        if (results != null) {
            supportActionBar?.title = Html.fromHtml("<font color='#01345A'>${results.query}</font>")
        }

        // NEED TO GET THE LIST OF RESULTS
        var listOfSearchResults = results.results

        // Grab the search results and display it under the searchHistoryName
        val searchHistory_Name = findViewById<TextView?>(R.id.searchHistoryName)

        val searchTitleList = arrayListOf<String>()

        if (listOfSearchResults.isNullOrEmpty()){

            searchHistory_Name.setText("No Search Results")

        } else {

            // Put the string text in the array of list
            for(items in results?.results!!){
                try {
                    when{
                        items.title == null->{
                            searchTitleList.add("<no announcements found>")
                        }
                        else-> {
                            items.title?.let{searchTitleList.add(it)}
                        }
                    }
                } catch (e: IOException){
                    Log.e("DigiPack", "Search result error: %s".format(e.toString()))
                }
            }

            // Then put that text in the textView
            val firstName: String = searchTitleList[0]
            searchHistory_Name?.text = firstName
        }


        // Calls the network detector class
        networkMonitor.result = { isAvailable, type ->
            runOnUiThread {
                when (isAvailable) {
                    true -> {
                        when (type) {
                            //changed this to only call the server once since we dont care what type
                            //of connection is happening currently
                            ConnectionType.Wifi, ConnectionType.Cellular  -> {
                                clouds.setImageResource(R.drawable.sun_connection)
                            }
                            else -> { }
                        }
                    }
                    false -> {
                        clouds.setImageResource(R.drawable.networkclouds)
                        //internet_connection.text = "No Connection"

                    }
                }
            }
        }

        // Add the list of results
        var classHomework = ArrayList<String>()

        for(items in results.results!!){
            try{
                when{
                    items.title == null->{
                        classHomework.add("<no courseWorkId found>")
                    }
                    else ->{
                        items.title?.let { classHomework.add(it) }
                    }
                }
            }catch (e: IOException){
                Log.e("DigiPack", "Class assignment error: %s".format(e.toString()))
            }
        }

        var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classHomework)
        resultDescriptions.adapter = adapterView

        resultDescriptions.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id->
            var courseDetail = results.results!![position]
            var resultName = courseDetail.title.toString()
            var resultSnippet = courseDetail.snippet.toString()
            var resultLink = courseDetail.link.toString()

            val intent = Intent(this, popUp::class.java)
            intent.putExtra("popupVersion", true)
            intent.putExtra("popuptitle", resultName)
            intent.putExtra("popuptext", "Description: " + resultSnippet)
            intent.putExtra("popupduedate", "Link: " + resultLink )


            startActivity(intent)

        }
    }

    // Network connection detector
    override fun onResume() {
        super.onResume()
        networkMonitor.register()
    }

    // Network connection detector
    override fun onStop() {
        super.onStop()
        networkMonitor.unregister()
    }
}



