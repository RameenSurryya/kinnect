package com.rameen.i230806.ui.chat

import android.os.Bundle
import com.rameen.i230806.databinding.ActivityChatsBinding
import com.rameen.i230806.ui.BaseActivity

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
            row.setOnClickListener { openScreen(ChatActivity::class.java) }
        }
    }
}
