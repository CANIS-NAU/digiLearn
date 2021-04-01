package com.example.digipack

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class classCourseDetails : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_course_details)
    }
    
    // need fixing
    // supposed to have the json data from the listview intent on the gClassActivity
    val ss:String = intent.getStringExtra("announcements").toString()
}

