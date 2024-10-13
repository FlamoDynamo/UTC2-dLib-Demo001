from pyteal import *

def approval_program():
    # Ebook Contract
    on_creation_ebook = Seq([
        App.globalPut(Bytes("ebook_owner"), Txn.sender()),
        App.globalPut(Bytes("ebook_id"), Int(0)),
        Return(Int(1))
    ])

    on_create_ebook = Seq([
        App.globalPut(
            Bytes("ebook_{}".format(App.globalGet(Bytes("ebook_id")))),
            Txn.sender()
        ),
        App.globalPut(Bytes("ebook_id"), App.globalGet(Bytes("ebook_id")) + Int(1)),
        Return(Int(1))
    ])

    on_fetch_all_ebooks = Seq([
        Return(App.globalGet(Bytes("ebook_id")))
    ])

    # Profile Contract
    on_creation_profile = Seq([
        App.globalPut(Bytes("profile_owner"), Txn.sender()),
        App.globalPut(Bytes("profile_id"), Int(0)),
        Return(Int(1))
    ])

    on_create_profile = Seq([
        App.globalPut(
            Bytes("profile_{}".format(App.globalGet(Bytes("profile_id")))),
            Txn.sender()
        ),
        App.globalPut(Bytes("profile_id"), App.globalGet(Bytes("profile_id")) + Int(1)),
        Return(Int(1))
    ])

    on_fetch_all_profiles = Seq([
        Return(App.globalGet(Bytes("profile_id")))
    ])

    # VideoBook Contract
    on_creation_video = Seq([
        App.globalPut(Bytes("video_owner"), Txn.sender()),
        App.globalPut(Bytes("video_id"), Int(0)),
        Return(Int(1))
    ])

    on_create_video = Seq([
        App.globalPut(
            Bytes("video_{}".format(App.globalGet(Bytes("video_id")))),
            Txn.sender()
        ),
        App.globalPut(Bytes("video_id"), App.globalGet(Bytes("video_id")) + Int(1)),
        Return(Int(1))
    ])

    on_fetch_all_videos = Seq([
        Return(App.globalGet(Bytes("video_id")))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation_ebook],
        [Txn.application_id() != Int(0), on_create_ebook],
        [Txn.application_id() != Int(0), on_fetch_all_ebooks],
        [Txn.application_id() == Int(0), on_creation_profile],
        [Txn.application_id() != Int(0), on_create_profile],
        [Txn.application_id() != Int(0), on_fetch_all_profiles],
        [Txn.application_id() == Int(0), on_creation_video],
        [Txn.application_id() != Int(0), on_create_video],
        [Txn.application_id() != Int(0), on_fetch_all_videos],
    )

    return program

def clear_state_program():
    return Return(Int(1))

compiled_program = compileTeal(approval_program(), mode=Mode.Application)
compiled_clear = compileTeal(clear_state_program(), mode=Mode.Application)

# Lưu mã TEAL vào file
with open("approval.teal", "w") as approval_file:
    approval_file.write(compiled_program)

with open("clear.teal", "w") as clear_file:
    clear_file.write(compiled_clear)

# Print the compiled code
print("Approval Program:")
print(compiled_program)
print("Clear State Program:")
print(compiled_clear)