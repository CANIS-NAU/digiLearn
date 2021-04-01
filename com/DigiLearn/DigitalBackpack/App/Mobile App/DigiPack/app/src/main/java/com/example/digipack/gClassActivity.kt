package com.example.digipack

import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import org.json.JSONObject
import java.io.IOException

class gClassActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gclass)

        var classnames = ArrayList<String>()
        var classids = ArrayList<String>()

        var gso = intent.getBundleExtra("gsoData")
        var classlist = intent.getStringExtra("classJson")

        read_json(classnames, classids)
    }

    fun read_json(classnames: ArrayList<String>, classids:ArrayList<String>){
        try{
            var classtr : String? = intent.getStringExtra("classJson")
            var json = JSONObject(classtr)
        }catch(e: IOException){
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }
    }

}