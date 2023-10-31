"use client"

import Link from "next/link";

export default function Navbar() {
  return (
    <div className="flex p-2.5 items-end">
      <div className="justify-start items-center gap-8 flex ml-2">
        <ul className="menu menu-horizontal px-1 gap-5">
          {/* <Link href="/" className="">
            Logo
          </Link> */}
          <li>
            <Link href="/" className="w-18">
              <div className="text-[18px] text-[#195BA5]">My Dashboard</div>
            </Link>
          </li>
        </ul>
      </div>

      <div className="flex-1"></div>
      <ul className="menu menu-horizontal px-1 gap-5">
        <li>
          <Link href="/aboutus" className="w-18">
            <div className="text-[18px] text-[#195BA5]">About Us</div>
          </Link>
        </li>

        <li>
          <div className="flex justify-center items-center">
            <button className="w-[104px] h-8 py-1.5 bg-sky-700 rounded-[10px] border-2 border-sky-700 justify-center items-center flex text-white">
              <div className="text-[18px] font-[600]">Log In</div>
            </button>
          </div>
        </li>
      </ul>
    </div>
  )
}

