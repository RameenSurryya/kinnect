package com.rameen.i230806.ui.profile

import android.os.Bundle
import com.rameen.i230806.databinding.ActivityEditProfileBinding
import com.rameen.i230806.ui.BaseActivity

/**
 * 16 Edit profile. UI only: the fields hold static sample values and nothing is saved.
 *  - Cancel and Save both close this screen (finish), returning to Profile.
 *  - The Edit links, the camera badge and "Switch to professional mode" are visual only.
 */
class EditProfileActivity : BaseActivity() {

    private lateinit var binding: ActivityEditProfileBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEditProfileBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.tvCancel.setOnClickListener { finish() }
        binding.tvSave.setOnClickListener { finish() }

        // Cuts the cover photo to the frame's rounded corners (bg_photo_rounded);
        // XML only has this attribute from Android 12.
        binding.flCover.clipToOutline = true
    }
}
