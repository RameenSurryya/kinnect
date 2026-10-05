package com.rameen.kinnect.ui.home

import android.content.Intent
import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityHomeBinding
import com.rameen.kinnect.ui.BaseActivity
import com.rameen.kinnect.ui.profile.ProfileActivity

/**
 * 04 Home feed. UI only: every element is static sample content.
 *  - Top bar (wordmark, search, messenger) and the tabs are wired by BaseActivity.
 *  - Composer pill / image icon open Create post, the JW avatar opens your Profile.
 *  - "Create story" opens the Camera, a friend's story card opens the Story viewer.
 *  - Comment opens Comments; long-pressing Like opens the Reaction picker.
 *  - "...", X, Like (tap) and Share do nothing.
 */
class HomeActivity : BaseActivity() {

    private lateinit var binding: ActivityHomeBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupHomeTopBar()
        setupTopTabs(Tab.HOME)

        // Composer row
        binding.tvComposerAvatar.setOnClickListener { open(ProfileActivity::class.java) }
        binding.tvComposer.setOnClickListener { open(CreatePostActivity::class.java) }
        binding.ivComposerPhoto.setOnClickListener { open(CreatePostActivity::class.java) }

        // Stories row. clipToOutline cuts the photo and name strip to the card's rounded
        // corners (bg_story_card); XML only has this attribute from Android 12.
        binding.flCreateStory.setOnClickListener { open(CameraActivity::class.java) }
        for (card in listOf(binding.flStoryOmar, binding.flStorySara, binding.flStoryHamza)) {
            card.clipToOutline = true
            card.setOnClickListener { open(StoryViewerActivity::class.java) }
        }

        // Post actions
        binding.llComment.setOnClickListener { open(CommentsActivity::class.java) }
        binding.llLike.setOnLongClickListener {
            open(ReactionPickerActivity::class.java)
            true // the long press is handled, so no normal click follows
        }
    }

    /** Opens another screen with an explicit Intent; Back returns here. */
    private fun open(screen: Class<*>) {
        startActivity(Intent(this, screen))
    }
}
