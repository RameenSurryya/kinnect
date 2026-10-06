package com.rameen.kinnect.ui.chat

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityChatBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 21 Chat with Aisha Khan. UI only: every message is static sample content.
 *  - Back arrow returns to the Chats list.
 *  - The phone icon opens the Voice call screen.
 *  - Video, info and the input bar icons do nothing.
 */
class ChatActivity : BaseActivity() {

    private lateinit var binding: ActivityChatBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChatBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ivBack.setOnClickListener { finish() }
        binding.ivCall.setOnClickListener { openScreen("com.rameen.kinnect.ui.chat.VoiceCallActivity") }

        // Cuts the photo message to the frame's rounded corners (bg_chat_photo);
        // XML only has this attribute from Android 12.
        binding.flPhoto.clipToOutline = true
    }
}
