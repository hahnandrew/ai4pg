"use client"

import { logout, signInWithGoogle } from "../../../firebase/firebase";
import { useAuth } from "../../../contexts/AuthContext";
import Link from "next/link";
// import { useRouter } from 'next/router';
// import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation'



export default function Navbar() {
  const { user } = useAuth();
  // console.log(user)
  // const user = true;
  // const router = useRouter();
  const pathname = usePathname()
  // const pathname = "hell"
  // console.log('asdfasf')
  // console.log(user);

  return (
    <div className="flex p-2.5 items-end">
      <div className="justify-start items-center gap-8 flex ml-2">
        <ul className="menu menu-horizontal px-1 gap-5">
          <li>
            <Link href="/" className="w-18">
              <div className="text-[18px] text-[#195BA5]">Dashboard</div>
            </Link>
          </li>
          {/* {user ? <li className={`${pathname === '/' ? 'underline-offset-1 custom-active' : ''}`}>
            <Link href="/" className="w-18">
              <div className="text-[18px] text-[#195BA5]">Dashboard</div>
            </Link>
          </li> : <div></div>} */}
        </ul>
      </div>

      <div className="flex-1"></div>
      <ul className="menu menu-horizontal px-1 gap-5">
        {/* <li className={`${pathname === '/picture' ? 'underline' : ''}`}>
          <Link href="/picture" className="w-18">
            <div className="text-[18px] text-[#195BA5]">Picture</div>
          </Link>
        </li> */}
        <li>
          <Link href="/picture" className="w-18">
            <div className="text-[18px] text-[#195BA5]">Picture</div>
          </Link>
        </li>

        {/* <li className={`${pathname === '/questionnaire' ? 'underline-offset-1 custom-active' : ''}`}>
          <Link href="/questionnaire" className="w-18">
            <div className="text-[18px] text-[#195BA5]">Questionnaire</div>
          </Link>
        </li> */}
        <li>
          <Link href="/questionnaire" className="w-18">
            <div className="text-[18px] text-[#195BA5]">Questionnaire</div>
          </Link>
        </li>



        {/* <li className={`${pathname === '/about' ? 'underline-offset-1 custom-active' : ''}`}>
          <Link href="/about" className="w-18">
            <div className="text-[18px] text-[#195BA5]">About Us</div>
          </Link>
        </li> */}
        <li>
          <Link href="/about" className="w-18">
            <div className="text-[18px] text-[#195BA5]">About Us</div>
          </Link>
        </li>

        {
          user ? <div className="dropdown dropdown-hover dropdown-bottom dropdown-end">
            <div tabIndex={0} className={`btn btn-circle text-[18px] font-normal`}>{user.displayName?.charAt(0)}</div>
            <ul tabIndex={0} className="menu dropdown-content p-2 shadow bg-base-100 rounded-box w-52">
              <Link href="edit_profile">
                <li>Edit Profile</li>
              </Link>
              <button onClick={logout}>
                <li>Log Out</li>
              </button>
            </ul>
          </div> : <li>
            <div className="flex justify-center items-center">
              <button
                className="w-[104px] h-8 py-1.5 bg-sky-700 rounded-[10px] border-2 border-sky-700 justify-center items-center flex text-white"
                onClick={() => signInWithGoogle()}
              >
                <div className="text-[18px] font-[600]">Log In</div>
              </button>
            </div>
          </li>
        }
      </ul>
    </div>

  )
}

