package com.rameen.kinnect.ui.chat

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityChatsBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 20 Chats. UI only: the notes and conversations are static sample content.
 *  - Back arrow returns to the previous screen (Home).
 *  - Tapping any conversation opens the Chat screen.
 *  - Compose, search, notes and the bottom nav do nothing.
 */
class ChatsActivity : BaseActivity() {

    private lateinit var binding: ActivityChatsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChatsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ivBack.setOnClickListener { finish() }

        val rows = listOf(
            binding.llChatAisha, binding.llChatDesignCrew, binding.llChatLina,
            binding.llChatOmar, binding.llChatBilal, binding.llChatNoor,
        )
        for (row in rows) {
            row.setOnClickListener { openScreen("com.rameen.kinnect.ui.chat.ChatActivity") }
        }
    }
}
