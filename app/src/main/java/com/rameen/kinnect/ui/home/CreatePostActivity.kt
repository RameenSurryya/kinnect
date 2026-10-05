package com.rameen.kinnect.ui.home

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.R
import com.rameen.kinnect.databinding.ActivityCreatePostBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 07 Create post. UI only: the post text, chips and swatches are static sample content.
 *  - X (and system Back) return to Home; Post also just closes the screen.
 *  - Photo/video opens the Photo picker, Camera opens the Camera.
 *  - Public / Album chips, swatches and the other sheet rows do nothing.
 */
class CreatePostActivity : BaseActivity() {

    private lateinit var binding: ActivityCreatePostBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCreatePostBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBackButton(R.id.iv_close)
        binding.btnPost.setOnClickListener { finish() }

        // Photo picker is named by class name until screen 08 exists (openScreen skips it).
        binding.llPhotoVideo.setOnClickListener { openScreen("com.rameen.kinnect.ui.home.PhotoPickerActivity") }
        binding.llCamera.setOnClickListener { startActivity(Intent(this, CameraActivity::class.java)) }
    }
}
