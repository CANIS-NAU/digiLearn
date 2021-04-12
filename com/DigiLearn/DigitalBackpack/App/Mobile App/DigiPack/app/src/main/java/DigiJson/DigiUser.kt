package DigiJson

import com.google.gson.annotations.SerializedName
import kotlinx.serialization.Serializable

class DigiUser {

    @Serializable
    data class Jsuser(
        @SerializedName("userName")
        var userName: String? = null,
        @SerializedName("googleEmail")
        var email: String? = null,
        @SerializedName("googleId")
        var gid: String? = null
    ) : java.io.Serializable

    @Serializable
    data class JsauthTok (
        @SerializedName("googleAccessToken")
        var authToken: String? = null,
        @SerializedName("gooogleEmail")
        var email: String? = null
    )
}