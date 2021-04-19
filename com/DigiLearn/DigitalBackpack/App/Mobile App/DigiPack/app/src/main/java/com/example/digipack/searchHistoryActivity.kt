package com.example.digipack

import DigiJson.DigiSearch
import android.os.Bundle
import android.text.Html
import androidx.appcompat.app.AppCompatActivity

class searchHistoryActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val ui = intent.getBooleanExtra("ui", false)

        // Determines what UI to show to the user
        if(ui){
            setContentView(R.layout.activity_kid_search_history)
        }else{
            setContentView(R.layout.activity_search_history)
        }

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Search History</font>")



    }

    private fun populateHistory(searchlist: ArrayList<DigiSearch.Results>?){
        //if the search list is null, let the user know that they dont have any results to show
        if( searchlist != null){

        }else{
            //else populate the

        }
    }
}
