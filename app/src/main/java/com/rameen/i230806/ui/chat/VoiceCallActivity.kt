package com.rameen.i230806.ui.chat

import android.os.Bundle
import com.rameen.i230806.databinding.ActivityVoiceCallBinding
import com.rameen.i230806.ui.BaseActivity

/**
 * 22 Voice call with Ammi. UI only: no microphone, speaker or real call.
 *  - The red end-call button (and the system Back) return to the Chat screen.
 *  - Transcript, mute and speaker do nothing.
 */
class VoiceCallActivity : BaseActivity() {

    override val darkSystemBars = true // white status bar icons on the teal screen

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val binding = ActivityVoiceCallBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.ivEndCall.setOnClickListener { finish() }
    }
}
