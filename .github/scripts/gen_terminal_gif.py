"""Generate the animated neofetch-style terminal GIF used in the profile README."""

import sys

import gifos

USER_NAME = "DashTX707"


def main() -> None:
    stats = gifos.utils.fetch_github_stats(user_name=USER_NAME, include_all_commits=False)
    if stats is None:
        print("ERROR: failed to fetch GitHub stats")
        sys.exit(1)

    top_langs = ", ".join(name for name, _ in stats.languages_sorted[:5]) or "n/a"

    t = gifos.Terminal(width=700, height=360, xpad=14, ypad=14)
    t.set_prompt("guest@dashtx707:~$ ")
    t.set_fps(10)

    row = 1
    t.gen_prompt(row_num=row)
    t.gen_typing_text(text="whoami", row_num=row, contin=True, speed=8)

    row += 1
    t.gen_text(text="Ibrahim Abdlrazik -- Threat Detection & CTI Specialist", row_num=row)
    row += 1
    t.gen_text(text="Senior SOC Consultant @ SIDF | MITRE ATT&CK Defender(TM)", row_num=row)
    t.clone_frame(count=20)  # hold so the whoami output is readable

    row += 2
    t.gen_prompt(row_num=row)
    t.gen_typing_text(text="neofetch --github", row_num=row, contin=True, speed=8)

    row += 1
    t.gen_text(text=f"Followers ............ {stats.total_followers}", row_num=row)
    row += 1
    t.gen_text(text=f"Repo contributions ... {stats.total_repo_contributions}", row_num=row)
    row += 1
    t.gen_text(text=f"Commits (last yr) .... {stats.total_commits_last_year}", row_num=row)
    row += 1
    t.gen_text(
        text=f"PRs merged ........... {stats.total_pull_requests_merged}/{stats.total_pull_requests_made}",
        row_num=row,
    )
    row += 1
    t.gen_text(text=f"Stars earned ......... {stats.total_stargazers}", row_num=row)
    row += 1
    t.gen_text(text=f"Issues opened ........ {stats.total_issues}", row_num=row)
    row += 1
    t.gen_text(text=f"PR reviews ........... {stats.total_pull_requests_reviewed}", row_num=row)
    row += 1
    t.gen_text(text=f"GitHub rank .......... {stats.user_rank}", row_num=row)
    row += 1
    t.gen_text(text=f"Top languages ........ {top_langs}", row_num=row)

    row += 2
    t.gen_prompt(row_num=row)
    t.clone_frame(count=80)  # hold the full neofetch output so it's actually readable

    t.gen_gif()


if __name__ == "__main__":
    main()
