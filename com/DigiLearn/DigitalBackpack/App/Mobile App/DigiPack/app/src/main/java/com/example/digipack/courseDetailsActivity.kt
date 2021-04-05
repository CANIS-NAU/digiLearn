package com.example.digipack

import android.os.Bundle
import android.text.Html
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_course_details.*
import kotlinx.android.synthetic.main.activity_gclass.*
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json

class courseDetailsActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_course_details)

        //unpack intent to get course data
        var cstring = intent.getStringExtra("course")
        print("cstring $cstring")
        var course = cstring?.let { Json.decodeFromString<DigiJson.Course>(it) }
        Log.i(getString(R.string.app_name), course.toString())

        // Change title
        if (course != null) {
            supportActionBar?.title = Html.fromHtml("<font color='#01345A'>${course.coursename}</font>")
        }







    }



}