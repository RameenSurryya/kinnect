package com.rameen.kinnect.ui.home

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityStoryEditorBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 10 Story editor. Visual only: the photo and the sticker are static.
 *  - The arrow and "Your story" open Your story.
 *  - X (and system Back) return to the camera.
 *  - The tool circles and "Close friends" do nothing.
 */
class StoryEditorActivity : BaseActivity() {
    override val darkSystemBars = true // white status bar icons on the black screen

    private lateinit var binding: ActivityStoryEditorBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityStoryEditorBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Cut the photo to the rounded corners of its background shape (XML cannot do this).
        binding.flViewport.clipToOutline = true

        binding.ivClose.setOnClickListener { finish() }
        binding.ivNext.setOnClickListener { openYourStory() }
        binding.llYourStory.setOnClickListener { openYourStory() }
    }

    /** Opens Your story (12) with an explicit Intent. */
    private fun openYourStory() = startActivity(Intent(this, YourStoryActivity::class.java))
}
