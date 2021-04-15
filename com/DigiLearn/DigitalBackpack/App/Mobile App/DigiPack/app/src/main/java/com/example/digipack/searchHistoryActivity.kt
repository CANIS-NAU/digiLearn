package com.example.digipack

import android.os.Bundle
import android.text.Html
import androidx.appcompat.app.AppCompatActivity

class searchHistoryActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search_history)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Search</font>")

    }
}
