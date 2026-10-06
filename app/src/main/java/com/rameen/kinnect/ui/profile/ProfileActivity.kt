package com.rameen.kinnect.ui.profile

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityProfileBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 15 Profile (your own profile). UI only: every element is static sample content.
 *  - The back arrow closes this screen (finish), returning to the previous one.
 *  - "Edit profile" opens the Edit profile screen.
 *  - Search, the camera badges, Add to story, "...", the pills and Find friends are visual only.
 */
class ProfileActivity : BaseActivity() {

    private lateinit var binding: ActivityProfileBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityProfileBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ivBack.setOnClickListener { finish() }
        binding.llEditProfile.setOnClickListener {
            startActivity(Intent(this, EditProfileActivity::class.java))
        }
    }
}
