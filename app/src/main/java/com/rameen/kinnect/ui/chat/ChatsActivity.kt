package com.rameen.kinnect.ui.chat

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityChatsBinding
import com.rameen.kinnect.ui.BaseActivity

/** 20 Chats (placeholder until the screen is built). */
class ChatsActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityChatsBinding.inflate(layoutInflater).root)
    }
}
