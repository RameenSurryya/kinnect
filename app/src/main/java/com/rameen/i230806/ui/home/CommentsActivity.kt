package com.rameen.i230806.ui.home

import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityCommentsBinding
import com.rameen.i230806.ui.BaseActivity

/**
 * 06 Comments. UI only: the comments, replies and reply bar are static sample content.
 * The back arrow returns to Home; everything else (sort pill, Like / Reply, Cancel, camera,
 * emoji, send) is visual only.
 */
class CommentsActivity : BaseActivity() {

    private lateinit var binding: ActivityCommentsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCommentsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBackButton(R.id.iv_back)

        // Cuts the photo comment to its 18dp rounded background (XML only has this from Android 12).
        binding.ivCommentPhoto.clipToOutline = true
    }
}
