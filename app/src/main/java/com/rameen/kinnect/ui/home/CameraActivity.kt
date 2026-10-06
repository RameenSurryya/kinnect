package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityCameraBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 09 Camera. Visual only: no real camera, the picture is a placeholder drawable.
 *  - The shutter opens the Story editor.
 *  - X (and system Back) return to the previous screen.
 *  - Brightness, gallery, flash, flip, effects and the mode labels do nothing.
 */
class CameraActivity : BaseActivity() {
    override val darkSystemBars = true // white status bar icons on the black screen

    private lateinit var binding: ActivityCameraBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCameraBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Cut the photo to the rounded corners of its background shape (XML cannot do this).
        binding.flViewport.clipToOutline = true
        binding.ivGallery.clipToOutline = true

        binding.ivClose.setOnClickListener { finish() }
        binding.ivShutter.setOnClickListener {
            openScreen("com.rameen.kinnect.ui.home.StoryEditorActivity")
        }
    }
}
