package com.rameen.kinnect.ui.home

import android.content.Intent
import android.os.Bundle
import androidx.activity.addCallback
import com.rameen.kinnect.databinding.ActivityYourStoryBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 12 Your story. Visual only: the photo, sticker, hearts and "Seen by" are static.
 *  - X (and system Back) go back to Home, skipping the camera and the editor.
 *  - Create, Highlight, Send and More do nothing.
 */
class YourStoryActivity : BaseActivity() {
    override val darkSystemBars = true // white status bar icons on the black screen

    private lateinit var binding: ActivityYourStoryBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityYourStoryBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Cut the photo to the rounded corners of its background shape (XML cannot do this).
        binding.flViewport.clipToOutline = true

        binding.ivClose.setOnClickListener { closeToHome() }
        onBackPressedDispatcher.addCallback(this) { closeToHome() }
    }

    /**
     * The story is posted, so closing it returns to Home. CLEAR_TOP closes every screen above
     * Home (camera, story editor); SINGLE_TOP reuses the Home that is already open.
     */
    private fun closeToHome() {
        startActivity(
            Intent(this, HomeActivity::class.java)
                .addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP)
        )
        finish()
    }
}
