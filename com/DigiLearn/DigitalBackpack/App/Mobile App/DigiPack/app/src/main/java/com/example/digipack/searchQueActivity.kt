package com.example.digipack

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView


class searchQueActivity : AppCompatActivity() {

    var userQuestion: String? = null
    var nameInput: EditText? = null
    var submitButton: Button? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search_que)
        nameInput = findViewById<View>(R.id.nameInput) as EditText
        val userQues = findViewById<TextView>(R.id.user_question)

        submitButton = findViewById<View>(R.id.submitButton) as Button

        submitButton!!.setOnClickListener {
            userQuestion = nameInput!!.text.toString()
            userQues.setText(userQuestion)
            println("=========================")

        }
    }
}