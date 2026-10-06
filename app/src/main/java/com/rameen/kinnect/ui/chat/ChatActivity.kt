package com.rameen.kinnect.ui.chat

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityChatBinding
import com.rameen.kinnect.ui.BaseActivity

/** 21 Chat (placeholder until the screen is built). */
class ChatActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityChatBinding.inflate(layoutInflater).root)
    }
}
