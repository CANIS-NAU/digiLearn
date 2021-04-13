package com.example.digipack

import DigiJson.DigiSearch
import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_gsearch.*
import java.io.IOException

class gSearchActivity : AppCompatActivity(){

    // Call the network detector tool
    private val networkMonitor = networkDetectorTool(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gsearch)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Search</font>")


        var guser = intent.getSerializableExtra("guser") as GUser
        var queries = intent.getSerializableExtra("resultslist") as DigiSearch.DigiRes
        var resultslist = queries.resultslist

        if( resultslist != null ){
            write_to_ui_and_listen(guser, resultslist)
        }

        newQueryButton.setOnClickListener {
            //allow them to make a new query and send it to the server if theres a connection
            //probably going to need yet another page for this one
        }

    }

    private fun write_to_ui_and_listen(guser: GUser, resultslist: ArrayList<DigiSearch.Results>) {
        var queryDetails = Intent()
        queryDetails.putExtra("guser", guser)
        try{
            var querylist = ArrayList<String>()
            for(i in resultslist){
                when (i.query) {
                    null -> {
                        querylist.add("<no query string found>")
                    }
                    else -> {
                        querylist.add(i.query!!)
                    }
                }
            }

            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, querylist )
            json_info.adapter = adapterView

            json_info.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id ->
                // do something with the query
                //probably gonna need another page for this
                queryDetails.putExtra("results", resultslist[position])
                this.startActivity(queryDetails)
            }
        }catch (e: IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "gSearchActivity write_to_ui error: %s".format(e.toString()))
        }
    }
}