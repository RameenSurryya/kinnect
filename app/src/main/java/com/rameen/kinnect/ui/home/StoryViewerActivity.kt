package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityStoryViewerBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 11 Story viewer (Omar Farooq's story). Visual only: the photo, progress bar and sticker are static.
 *  - X (and system Back) return to Home.
 *  - "...", "Send message..." and the reactions do nothing.
 */
class StoryViewerActivity : BaseActivity() {
    override val darkSystemBars = true // white status bar icons on the black screen

    private lateinit var binding: ActivityStoryViewerBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityStoryViewerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Cut the photo to the rounded corners of its background shape (XML cannot do this).
        binding.flViewport.clipToOutline = true

        binding.ivClose.setOnClickListener { finish() }
    }
}
