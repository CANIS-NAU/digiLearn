package DigiJson

import kotlinx.serialization.Serializable

class GUserJson {

    @Serializable
    data class GUser(
        var email: String? = null,
        var firstName: String? = null,
        var lastName: String? = null,
        var idToken: String? = null,
        var userID: String? = null,
        var authCode: String? = null
    ) : java.io.Serializable
}