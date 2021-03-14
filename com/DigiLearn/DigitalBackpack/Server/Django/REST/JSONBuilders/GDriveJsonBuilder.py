import json

_none = type(None)

def createfilejson(fileobj):
    ##  this json object was pulled from https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/drive_v3.files.html#create
    # some of it has been removed for ease of use/usefulness to us but there might be issues with not having all/enough data to upload correctly
    # so thats why im leaving the link here until we get to testing
    # commented out values are ones I dont think we need but might need for it to work
    gdrivejson = { # The metadata for a file.
      #"hasThumbnail": True or False, # Whether this file has a thumbnail. This does not indicate whether the requesting app has access to the thumbnail. To check access, look for the presence of the thumbnailLink field.
      #"modifiedByMeTime": "A String", # The last time the file was modified by the user (RFC 3339 date-time).
      #"thumbnailLink": "A String", # A short-lived link to the file's thumbnail, if available. Typically lasts on the order of hours. Only populated when the requesting app can access the file's content.
      #"thumbnailVersion": "A String", # The thumbnail version for use in thumbnail cache invalidation.
      "explicitlyTrashed": False, # Whether the file has been explicitly trashed, as opposed to recursively trashed from a parent folder.
      "isAppAuthorized": True, # Whether the file was created or opened by the requesting app.
      "ownedByMe": True, # Whether the user owns the file. Not populated for items in shared drives.
      #"viewedByMeTime": "A String", # The last time the file was viewed by the user (RFC 3339 date-time).
      "id": "A String", # The ID of the file.
      "size": "A String", # The size of the file's content in bytes. This is only applicable to files with binary content in Google Drive.
"""
      "videoMediaMetadata": { # Additional metadata about video media. This may not be available immediately upon upload.
        "width": 42, # The width of the video in pixels.
        "durationMillis": "A String", # The duration of the video in milliseconds.
        "height": 42, # The height of the video in pixels.
      },
      "lastModifyingUser": { # Information about a Drive user. # The last user to modify the file.
        "me": True or False, # Whether this user is the requesting user.
        "kind": "drive#user", # Identifies what kind of resource this is. Value: the fixed string "drive#user".
        "displayName": "A String", # A plain text displayable name for this user.
        "permissionId": "A String", # The user's ID as visible in Permission resources.
        "emailAddress": "A String", # The email address of the user. This may not be present in certain contexts if the user has not made their email address visible to the requester.
        "photoLink": "A String", # A link to the user's profile photo, if available.
      },
"""
      "appProperties": { # A collection of arbitrary key-value pairs which are private to the requesting app.
          # Entries with null values are cleared in update and copy requests.
        "a_key": "A String",  # i think this is from the credentials.json
      },
"""
      "capabilities": { # Capabilities the current user has on this file. Each capability corresponds to a fine-grained action that a user may take.
        "canMoveItemOutOfDrive": True or False, # Whether the current user can move this item outside of this drive by changing its parent. Note that a request to change the parent of the item may still fail depending on the new parent that is being added.
        "canUntrash": True or False, # Whether the current user can restore this file from trash.
        "canMoveItemWithinTeamDrive": True or False, # Deprecated - use canMoveItemWithinDrive instead.
        "canDeleteChildren": True or False, # Whether the current user can delete children of this folder. This is false when the item is not a folder. Only populated for items in shared drives.
        "canMoveChildrenWithinTeamDrive": True or False, # Deprecated - use canMoveChildrenWithinDrive instead.
        "canListChildren": True or False, # Whether the current user can list the children of this folder. This is always false when the item is not a folder.
        "canRename": True or False, # Whether the current user can rename this file.
        "canModifyContent": True or False, # Whether the current user can modify the content of this file.
        "canReadDrive": True or False, # Whether the current user can read the shared drive to which this file belongs. Only populated for items in shared drives.
        "canAddChildren": True or False, # Whether the current user can add children to this folder. This is always false when the item is not a folder.
        "canShare": True or False, # Whether the current user can modify the sharing settings for this file.
        "canTrashChildren": True or False, # Whether the current user can trash children of this folder. This is false when the item is not a folder. Only populated for items in shared drives.
        "canAddMyDriveParent": True or False, # Whether the current user can add a parent for the item without removing an existing parent in the same request. Not populated for shared drive files.
        "canMoveChildrenWithinDrive": True or False, # Whether the current user can move children of this folder within the shared drive. This is false when the item is not a folder. Only populated for items in shared drives.
        "canReadRevisions": True or False, # Whether the current user can read the revisions resource of this file. For a shared drive item, whether revisions of non-folder descendants of this item, or this item itself if it is not a folder, can be read.
        "canMoveItemWithinDrive": True or False, # Whether the current user can move this item within this shared drive. Note that a request to change the parent of the item may still fail depending on the new parent that is being added. Only populated for items in shared drives.
        "canCopy": True or False, # Whether the current user can copy this file. For an item in a shared drive, whether the current user can copy non-folder descendants of this item, or this item itself if it is not a folder.
        "canMoveItemIntoTeamDrive": True or False, # Deprecated - use canMoveItemOutOfDrive instead.
        "canMoveItemOutOfTeamDrive": True or False, # Deprecated - use canMoveItemOutOfDrive instead.
        "canComment": True or False, # Whether the current user can comment on this file.
        "canMoveChildrenOutOfDrive": True or False, # Whether the current user can move children of this folder outside of the shared drive. This is false when the item is not a folder. Only populated for items in shared drives.
        "canChangeViewersCanCopyContent": True or False, # Deprecated
        "canTrash": True or False, # Whether the current user can move this file to trash.
        "canRemoveMyDriveParent": True or False, # Whether the current user can remove a parent from the item without adding another parent in the same request. Not populated for shared drive files.
        "canDelete": True or False, # Whether the current user can delete this file.
        "canMoveTeamDriveItem": True or False, # Deprecated - use canMoveItemWithinDrive or canMoveItemOutOfDrive instead.
        "canDownload": True or False, # Whether the current user can download this file.
        "canChangeCopyRequiresWriterPermission": True or False, # Whether the current user can change the copyRequiresWriterPermission restriction of this file.
        "canMoveChildrenOutOfTeamDrive": True or False, # Deprecated - use canMoveChildrenOutOfDrive instead.
        "canRemoveChildren": True or False, # Whether the current user can remove children from this folder. This is always false when the item is not a folder. For a folder in a shared drive, use canDeleteChildren or canTrashChildren instead.
        "canReadTeamDrive": True or False, # Deprecated - use canReadDrive instead.
        "canEdit": True or False, # Whether the current user can edit this file. Other factors may limit the type of changes a user can make to a file. For example, see canChangeCopyRequiresWriterPermission or canModifyContent.
      },
"""
      "version": "1", # A monotonically increasing version number for the file. This reflects every change made to the file on the server, even those not visible to the user.
      "parents": [ # The IDs of the parent folders which contain the file.
          # If not specified as part of a create request, the file will be placed directly in the user's My Drive folder. If not specified as part of a copy request, the file will inherit any discoverable parents of the source file. Update requests must use the addParents and removeParents parameters to modify the parents list.
        "A String",
      ],
      "shared": True or False, # Whether the file has been shared. Not populated for items in shared drives.
      "copyRequiresWriterPermission": True or False, # Whether the options to copy, print, or download this file, should be disabled for readers and commenters.
      "fullFileExtension": "A String", # The full file extension extracted from the name field. May contain multiple concatenated extensions, such as "tar.gz". This is only available for files with binary content in Google Drive.
          # This is automatically updated when the name field changes, however it is not cleared if the new name does not contain a valid extension.
      "originalFilename": "A String", # The original filename of the uploaded content if available, or else the original value of the name field. This is only available for files with binary content in Google Drive.
      "description": "A String", # A short description of the file.
      "modifiedTime": "A String", # The last time the file was modified by anyone (RFC 3339 date-time).
          # Note that setting modifiedTime will also update modifiedByMeTime for the user.
      "viewedByMe": True, # Whether the file has been viewed by this user.
      "modifiedByMe": True, # Whether the file has been modified by this user.
      "owners": [ # The owners of the file. Currently, only certain legacy files may have more than one owner. Not populated for items in shared drives.
        { # Information about a Drive user.
          "me": True, # Whether this user is the requesting user.
          "kind": "drive#user", # Identifies what kind of resource this is. Value: the fixed string "drive#user".
          "displayName": "A String", # A plain text displayable name for this user.
          "permissionId": "A String", # The user's ID as visible in Permission resources.
          "emailAddress": "A String", # The email address of the user. This may not be present in certain contexts if the user has not made their email address visible to the requester.
          "photoLink": "A String", # A link to the user's profile photo, if available.
        },
      ],
      "createdTime": "A String", # The time at which the file was created (RFC 3339 date-time).
      "quotaBytesUsed": "A String", # The number of storage quota bytes used by the file. This includes the head revision as well as previous revisions with keepForever enabled.
      "properties": { # A collection of arbitrary key-value pairs which are visible to all apps.
          # Entries with null values are cleared in update and copy requests.
        "a_key": "A String",
      },
      "md5Checksum": "A String", # The MD5 checksum for the content of the file. This is only applicable to files with binary content in Google Drive.
      "iconLink": "A String", # A static, unauthenticated link to the file's icon.
      "imageMediaMetadata": { # Additional metadata about image media, if available.
        "exposureBias": 3.14, # The exposure bias of the photo (APEX value).
        "exposureTime": 3.14, # The length of the exposure, in seconds.
        "cameraMake": "A String", # The make of the camera used to create the photo.
        "maxApertureValue": 3.14, # The smallest f-number of the lens at the focal length used to create the photo (APEX value).
        "width": 42, # The width of the image in pixels.
        "focalLength": 3.14, # The focal length used to create the photo, in millimeters.
        "exposureMode": "A String", # The exposure mode used to create the photo.
        "colorSpace": "A String", # The color space of the photo.
        "location": { # Geographic location information stored in the image.
          "latitude": 3.14, # The latitude stored in the image.
          "altitude": 3.14, # The altitude stored in the image.
          "longitude": 3.14, # The longitude stored in the image.
        },
        "subjectDistance": 42, # The distance to the subject of the photo, in meters.
        "height": 42, # The height of the image in pixels.
        "lens": "A String", # The lens used to create the photo.
        "isoSpeed": 42, # The ISO speed used to create the photo.
        "meteringMode": "A String", # The metering mode used to create the photo.
        "flashUsed": True or False, # Whether a flash was used to create the photo.
        "time": "A String", # The date and time the photo was taken (EXIF DateTime).
        "aperture": 3.14, # The aperture used to create the photo (f-number).
        "rotation": 42, # The number of clockwise 90 degree rotations applied from the image's original orientation.
        "sensor": "A String", # The type of sensor used to create the photo.
        "whiteBalance": "A String", # The white balance mode used to create the photo.
        "cameraModel": "A String", # The model of the camera used to create the photo.
      },
      "kind": "drive#file", # Identifies what kind of resource this is. Value: the fixed string "drive#file".
      "name": "A String", # The name of the file. This is not necessarily unique within a folder. Note that for immutable items such as the top level folders of shared drives, My Drive root folder, and Application Data folder the name is constant.
      "webContentLink": "A String", # A link for downloading the content of the file in a browser. This is only available for files with binary content in Google Drive.
      "trashingUser": { # Information about a Drive user. # If the file has been explicitly trashed, the user who trashed it. Only populated for items in shared drives.
        "me": True or False, # Whether this user is the requesting user.
        "kind": "drive#user", # Identifies what kind of resource this is. Value: the fixed string "drive#user".
        "displayName": "A String", # A plain text displayable name for this user.
        "permissionId": "A String", # The user's ID as visible in Permission resources.
        "emailAddress": "A String", # The email address of the user. This may not be present in certain contexts if the user has not made their email address visible to the requester.
        "photoLink": "A String", # A link to the user's profile photo, if available.
      },
      "driveId": "A String", # ID of the shared drive the file resides in. Only populated for items in shared drives.
      "spaces": [ # The list of spaces which contain the file. The currently supported values are 'drive', 'appDataFolder' and 'photos'.
        "drive",
      ],
      "permissionIds": [ # List of permission IDs for users with access to this file.
        "A String",
      ],
      "trashed": False, # Whether the file has been trashed, either explicitly or from a trashed parent folder. Only the owner may trash a file, and other users cannot see files in the owner's trash.
      "contentHints": { # Additional information about the content of the file. These fields are never populated in responses.
        "indexableText": "A String", # Text to be indexed for the file to improve fullText queries. This is limited to 128KB in length and may contain HTML elements.
        "thumbnail": { # A thumbnail for the file. This will only be used if Google Drive cannot generate a standard thumbnail.
          "mimeType": "A String", # The MIME type of the thumbnail.
          "image": "A String", # The thumbnail data encoded with URL-safe Base64 (RFC 4648 section 5).
        },
      },
      "fileExtension": "A String", # The final component of fullFileExtension. This is only available for files with binary content in Google Drive.
      "hasAugmentedPermissions": True or False, # Whether there are permissions directly on this file. This field is only populated for items in shared drives.
      "permissions": [ # The full list of permissions for the file. This is only available if the requesting user can share the file. Not populated for items in shared drives.
        { # A permission for a file. A permission grants a user, group, domain or the world access to a file or a folder hierarchy.
          "domain": "A String", # The domain to which this permission refers.
          "displayName": "A String", # The "pretty" name of the value of the permission. The following is a list of examples for each type of permission:
              # - user - User's full name, as defined for their Google account, such as "Joe Smith."
              # - group - Name of the Google Group, such as "The Company Administrators."
              # - domain - String domain name, such as "thecompany.com."
              # - anyone - No displayName is present.
          "allowFileDiscovery": True or False, # Whether the permission allows the file to be discovered through search. This is only applicable for permissions of type domain or anyone.
          "deleted": True or False, # Whether the account associated with this permission has been deleted. This field only pertains to user and group permissions.
          "kind": "drive#permission", # Identifies what kind of resource this is. Value: the fixed string "drive#permission".
          "emailAddress": "A String", # The email address of the user or group to which this permission refers.
          "photoLink": "A String", # A link to the user's profile photo, if available.
          "permissionDetails": [ # Details of whether the permissions on this shared drive item are inherited or directly on this item. This is an output-only field which is present only for shared drive items.
            {
              "role": "A String", # The primary role for this user. While new values may be added in the future, the following are currently possible:
                  # - organizer
                  # - fileOrganizer
                  # - writer
                  # - commenter
                  # - reader
              "inheritedFrom": "A String", # The ID of the item from which this permission is inherited. This is an output-only field.
              "permissionType": "A String", # The permission type for this user. While new values may be added in future, the following are currently possible:
                  # - file
                  # - member
              "inherited": True or False, # Whether this permission is inherited. This field is always populated. This is an output-only field.
            },
          ],
          "expirationTime": "A String", # The time at which this permission will expire (RFC 3339 date-time). Expiration times have the following restrictions:
              # - They can only be set on user and group permissions
              # - The time must be in the future
              # - The time cannot be more than a year in the future
          "role": "A String", # The role granted by this permission. While new values may be supported in the future, the following are currently allowed:
              # - owner
              # - organizer
              # - fileOrganizer
              # - writer
              # - commenter
              # - reader
          "type": "A String", # The type of the grantee. Valid values are:
              # - user
              # - group
              # - domain
              # - anyone  When creating a permission, if type is user or group, you must provide an emailAddress for the user or group. When type is domain, you must provide a domain. There isn't extra information required for a anyone type.
          "id": "A String", # The ID of this permission. This is a unique identifier for the grantee, and is published in User resources as permissionId. IDs should be treated as opaque values.
        },
      ],
      "headRevisionId": "A String", # The ID of the file's head revision. This is currently only available for files with binary content in Google Drive.
    }

    return gdrivejson