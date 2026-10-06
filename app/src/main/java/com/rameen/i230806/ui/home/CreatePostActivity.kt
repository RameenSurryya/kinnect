package com.rameen.i230806.ui.home

import android.content.Intent
import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityCreatePostBinding
import com.rameen.i230806.ui.BaseActivity

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

        binding.llPhotoVideo.setOnClickListener { startActivity(Intent(this, PhotoPickerActivity::class.java)) }
        binding.llCamera.setOnClickListener { startActivity(Intent(this, CameraActivity::class.java)) }
    }
}
