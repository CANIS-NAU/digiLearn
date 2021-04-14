package com.example.digipack

import android.os.Bundle
import android.text.Html
import androidx.appcompat.app.AppCompatActivity

class gSearchActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val ui = intent.getBooleanExtra("ui", false)

        // Determines what UI to show to the user
        if(ui){
            setContentView(R.layout.activity_kid_glcass)
        }else{
            setContentView(R.layout.activity_gclass)
        }

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Search</font>")

    }
}