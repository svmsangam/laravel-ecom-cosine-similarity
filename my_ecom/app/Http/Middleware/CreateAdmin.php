<?php

namespace App\Http\Middleware;

use App\Models\Admin\Admin;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class CreateAdmin
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next)
    {
        $admin = Admin::count();
        if($admin === 0){
        $new_admin = new Admin();
        $new_admin->email = "admin@admin.com";
        $new_admin->password = Hash::make("admin@admin.com");
        $new_admin->save();
        }
        return $next($request);
    }
}
