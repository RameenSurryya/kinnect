package com.rameen.i230806.ui.home

import android.os.Bundle
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivityPhotoPickerBinding
import com.rameen.i230806.ui.BaseActivity

/**
 * 08 Photo picker. UI only: the preview, grid, selections and "0:23" are static sample content.
 *  - Cancel (and system Back) return to Create post.
 *  - Next (2) also closes this screen, back to Create post.
 *  - Recents, expand, SELECT MULTIPLE, the tiles and Gallery / Photo / Video do nothing.
 */
class PhotoPickerActivity : BaseActivity() {

    private lateinit var binding: ActivityPhotoPickerBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityPhotoPickerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBackButton(R.id.tv_cancel)
        binding.tvNext.setOnClickListener { finish() }
    }
}
