package com.rameen.kinnect.ui.profile

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityOtherProfileBinding
import com.rameen.kinnect.ui.BaseActivity
import com.rameen.kinnect.ui.chat.ChatActivity

/**
 * 17 Other profile (Omar Farooq). UI only: every element is static sample content.
 *  - The back arrow closes this screen (finish), returning to the previous one.
 *  - "Message" opens the Chat screen.
 *  - Search, Add friend, "...", the mutual friends line and See all are visual only.
 */
class OtherProfileActivity : BaseActivity() {

    private lateinit var binding: ActivityOtherProfileBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOtherProfileBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ivBack.setOnClickListener { finish() }
        binding.llMessage.setOnClickListener {
            startActivity(Intent(this, ChatActivity::class.java))
        }

        // Cuts each photo to its tile's rounded corners (bg_gallery_thumb);
        // XML only has this attribute from Android 12.
        binding.ivPhoto1.clipToOutline = true
        binding.ivPhoto2.clipToOutline = true
        binding.ivPhoto3.clipToOutline = true
    }
}
