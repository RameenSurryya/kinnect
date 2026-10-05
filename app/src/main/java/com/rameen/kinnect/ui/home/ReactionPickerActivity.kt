package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityReactionPickerBinding
import com.rameen.kinnect.ui.BaseActivity

/**
 * 05 Reaction picker, opened by long-pressing Like on Home. UI only.
 * The post behind is dimmed; the white pill shows the six reactions with Love raised.
 * The back arrow, a tap on the dim area or a tap on any reaction closes this screen
 * (finish()), which returns to Home underneath.
 */
class ReactionPickerActivity : BaseActivity() {

    private lateinit var binding: ActivityReactionPickerBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityReactionPickerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val closers = listOf(
            binding.ivBack, binding.vDim,
            binding.ivReactionLike, binding.ivReactionLove, binding.ivReactionHaha,
            binding.ivReactionWow, binding.ivReactionSad, binding.ivReactionAngry,
        )
        for (view in closers) {
            view.setOnClickListener { finish() }
        }
    }
}
