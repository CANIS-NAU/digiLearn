package com.example.digipack

import DigiJson.DigiDrive
import DigiJson.GUserJson.GUser
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_file_list_view.*
import util.FileDownloader
import java.io.IOException

const val PICK_PDF_FILE = 2

class FileListViewActivity : AppCompatActivity() {

    var url : String = ""
    private val networkMonitor = networkDetectorTool(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.i(getString(R.string.app_name), "FileListView: created")
        var layoutselect = intent.getBooleanExtra("layoutselection", false)
        if(layoutselect){
            setContentView(R.layout.kids_activity_file_list_view)
        }else{
            setContentView(R.layout.activity_file_list_view)
        }

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Files</font>")

        //initialization
        var context : Context = this
        var user = intent.getSerializableExtra("guser") as GUser
        var df = intent.getSerializableExtra("filelist") as DigiDrive.DF
        var filelist = df.Files

        //write to ui and listen for click
        if (filelist != null) {
            writeToUiAndListen(user, filelist, layoutselect)
        }

        // Looking for the file button connection
        val openFileButton = findViewById<Button>(R.id.openFileButton)
    }

    private fun writeToUiAndListen(user: GUser, files: ArrayList<DigiDrive.DigiFile>, layoutselect: Boolean)
    {
        var adapterView : ArrayAdapter<String>
        try{
            var filenamelist = ArrayList<String>()
            for(i in files){
                when{
                    i.fileName == null ->{
                        filenamelist.add("<no file name found>")
                    }
                    else -> {
                        i.fileName?.let { filenamelist.add(it) }
                    }
                }

            }
            if(layoutselect){
                adapterView = ArrayAdapter(this, R.layout.kids_list_textview, filenamelist)
            }else{
                adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, filenamelist)
            }

            json_info.adapter = adapterView

            // Creates an onclick listener when the user clicks on the driveID that would be referenced to driveID
            json_info.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id->
                //position is the index of the list item that corresponds to the button clicked
                //fileClicked(user, files, position)
                Toast.makeText(this, "File \"${filenamelist[position]} clicked", Toast.LENGTH_SHORT).show()

            }
        }catch (e: IOException){
            //handle errors eventually
            Log.e(getString(R.string.app_name), "FileListViewActivity write_to_ui error: %s".format(e.toString()))
        }
    }
/**
    private fun fileClicked(user: GUser, files: ArrayList<DigiDrive.DigiFile>, position: Int) {
        //build url
        //should probably not be a global value in prod
        url = getString(R.string.serverUrl).plus(getString(R.string.downloadUrl))
        url.plus("${files[position].fileName}")
        //make request to server for the server to download the file
        var server = ServerInteraction()
        server.requestFileForDownload(user, files[position], this)
        when{
            //download the file when the server responds positively
            (server.isReqFileSuccInitialized() && server.reqfilesucc.success == 1) -> {
                FileDownloader().getFile(this, url)
            }
        }
    }
**/
    // Checks if the requestCode is the same, if so then continue the sign in process
    override fun onActivityResult(requestCode: Int, resultCode: Int, resultData: Intent?) {
        super.onActivityResult(requestCode, resultCode, resultData)

        //after the user picks a pdf file
        if (requestCode == PICK_PDF_FILE){
            var uri: Uri? = null

            //if they successfully picked a file
            if (resultData != null) {
                //call an intent to open the file up; asks user to select an application with which to view pdf
                uri = resultData.data
                val intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(uri, "application/pdf")
                intent.setFlags( Intent.FLAG_GRANT_READ_URI_PERMISSION or
                                    Intent.FLAG_ACTIVITY_NO_HISTORY )
                startActivity(intent)
            }
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        FileDownloader().onRequestPermissionsResult(requestCode, permissions, grantResults)
    }

    override fun onResume() {
        super.onResume()
        networkMonitor.register()
    }

    override fun onStop() {
        super.onStop()
        networkMonitor.unregister()
    }

}